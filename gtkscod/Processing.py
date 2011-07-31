#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

from Detail import Detail
from ListenThread import ListenThread
from DevicesListModel import DevicesListModel
from ActionsModel import ActionsModel

from packagekitwrapper import PackageKitClient, PackageKitError 

class WindowProcessing():
	def __init__(self, parent = None):
		self.Parent = parent
		self.Detail = Detail(False, 1)
		self.lt = ListenThread(parent_class = self.add_new_device)
		self._install_akmods = False
		self._main_pko = None		#PackageKitClient()
		
		# right frame
		self.Detail.modules.connect('changed', self._handle_select_module)
		self.Detail.reset.connect('clicked', self._handle_rbb, 'reset')
		self.Detail.accept.connect('clicked', self._handle_rbb, 'accept')

	def _init_models(self):
		self.listView = self.Parent.listDev
		self.model = DevicesListModel(self)
		self.listView.set_model(self.model)
		self.devSelection = self.listView.get_selection()
		self.devSelection.set_mode(gtk.SELECTION_SINGLE)

		self.listViewActions = self.Parent.listAct
		self.act_model = ActionsModel(self)
		self.listViewActions.set_model(self.act_model)
		self.actSelection = self.listViewActions.get_selection()
		self.actSelection.set_mode(gtk.SELECTION_SINGLE)

		self.tvcolumn = gtk.TreeViewColumn('Actions ')
		self.listViewActions.append_column(self.tvcolumn)
		self.cellpb = gtk.CellRendererPixbuf()
		self.cell = gtk.CellRendererText()
		self.tvcolumn.pack_start(self.cellpb, False)
		self.tvcolumn.pack_start(self.cell, True)
		self.tvcolumn.set_attributes(self.cellpb, stock_id=1)
		self.tvcolumn.set_attributes(self.cell, text=0)

	def _init_pk(self):
		if self._main_pko is None:
			self._main_pko = PackageKitClient()

	def add_new_device(self, dev):
		print dev
		""" show device """
		self.Detail.entry.set_text(dev['name'])
		self.model.add_new_device(dev)
		""" show modules """
		moduleKeys = dev['modules'].iterkeys()
		for module in moduleKeys :
			self.Detail.modules.append_text(module)
		# uncomment for define the first store as default
		#self.Detail.modules.set_active(0)
		self.show_notification()

	def disen_device_notif(self, device_id, disable = False):
		if disable:
			self.lt.disable_device_notif(device_id)
		else:
			self.lt.enable_device_notif(device_id)

	def show_notification(self):
		self.Parent.window.show_all()

	def start_listen(self):
		self.lt.run()

	def _right_frame_apply(self, idx):
		d = self.model.device_by_index(idx)
		sel_cb_idx = self.Detail.modules.get_active_iter()
		if sel_cb_idx is None :
			print 'module not selected'
			return
		sel_module = str(self.Detail.modulesMod.get_value(sel_cb_idx, 0))
		if d is None : 
			print 'device not selected'
			return
		elif sel_module == d.current_driver() :
			print 'Driver is current'
			return

		self.act_model.remove_actions_by_devid(d.device_id(), sel_module)
		pkgsi = d.packages_to_install(sel_module)
		pkgsr = d.packages_to_remove(sel_module)
		print pkgsi, '<install||remove>', pkgsr
		if len(pkgsi) > 0:
			self.act_model.add_new_action(d.device_id(), 
							  sel_module, pkgsi, 0)
		if len(pkgsr) > 0:	  
			rem_mds = str(', ').join(d.device_modules(sel_module))
			self.act_model.add_new_action(d.device_id(), rem_mds, pkgsr, 1)
		d.set_selected_driver(sel_module)
		self.set_right_frame(idx)
	
	def _current_device(self, idx = None):
		cur_idx = idx
		if idx is None:
			model, curr_iter = self.devSelection.get_selected()
			if curr_iter is None :
				print 'Device Not Selected'
				return
			else :
				cur_idx = self.model.curr_row(curr_iter)
		return self.model.device_by_index(cur_idx)

	def set_right_frame(self, idx):
		self.Detail.modulesMod.clear()
		d = self._current_device(idx)
		"""print d.device_name(), ':', d.current_driver(), ':', \
			  d.device_modules(),':', d.selected_driver(),\
			  ':', len(self.Detail.modules)"""
		curdrv = ''
		if d.current_driver() is None or len(d.current_driver()) == 0:
			curdrv = 'Not installed'
		else:
			curdrv = '- %s -' % d.current_driver()
		#print curdrv, 'cur'
		self.Detail.modules.append_text(curdrv)

		self.Detail.entry.set_text(d.device_name())
		our_sel_idx = -1
		for m in d.device_modules():
			devmod = ''
			if m == d.current_driver():
				continue
			elif m == d.selected_driver():
				devmod = '* %s *' % m
				our_sel_idx = len(self.Detail.modules)
				#print our_sel_idx, 'our'
			else:
				devmod = '%s' % m
			#print devmod, 'dev'
			self.Detail.modules.append_text(devmod)

		if our_sel_idx != -1:
			self.Detail.modules.set_active(our_sel_idx)

	def _do_resolve_packages(self, pkgs, to_remove = False):
		if len(pkgs) == 0:
			return
		self._init_pk()
		pkc = self._main_pko #PackageKitClient()
		filt = 'none'
		if to_remove:
			filt = 'installed'
			pkg_ids = pkc.SearchNames(filt, pkgs)
			return pkg_ids
		pkg_ids = pkc.Resolve(filt, pkgs)

		return pkg_ids

	def _do_install_packages(self, pkgs):
		if len(pkgs) == 0:
			return
		print "Begin install packages"
		self._init_pk()
		pkc = self._main_pko #PackageKitClient()
		pkc.InstallPackages(pkgs)

	def _do_remove_packages(self, pkgs):
		if len(pkgs) == 0:
			return
		print "Begin remove packages"
		self._init_pk()
		pkc = self._main_pko #PackageKitClient()
		pkc.RemovePackages(pkgs)

	def _do_only_ids(self, pkgs):
		res_ids = []
		if pkgs is None:
			return res_ids
		if len(pkgs) == 0:
			return res_ids
		print pkgs
		for installed, id, summary in pkgs:
			res_ids.append(id)
		return res_ids

	def _debug_print_pkg_ids(self, pkg_ids):
		if pkg_ids is None:
			return
		elif len(pkg_ids) == 0:
			return
		for pi_info,pi_id,pi_sum in pkg_ids:
			print "+ %s (%s) installed: %s" % (pi_id, pi_sum, pi_info)
		

	def _do_act(self):
		pkgs_to_install, pkgs_to_remove = self.act_model.get_packages(self._install_akmods)

		# Resolve all packages
		pkg_ids_install = self._do_resolve_packages(pkgs_to_install)
		pkg_ids_remove = self._do_resolve_packages(pkgs_to_remove, True)

		self._do_remove_packages(self._do_only_ids(pkg_ids_remove))
		self._do_install_packages(self._do_only_ids(pkg_ids_install))

		print "Packages to install:"
		self._debug_print_pkg_ids(pkg_ids_install)
		
		print "Packages to remove:"
		self._debug_print_pkg_ids(pkg_ids_remove)
		dialog = gtk.Dialog(title = "Operations done", \
							parent = self.Parent.window, \
							flags = gtk.DIALOG_MODAL, \
							buttons = None)
		label = gtk.Label('All operations applied. You may reboot a system. Reboot now?')
		dialog.vbox.pack_start(label, True, True, 0)
		buttonOk = gtk.Button(stock = gtk.STOCK_OK)
		dialog.action_area.pack_start(buttonOk, True, True, 0)
		buttonNo = gtk.Button(stock = gtk.STOCK_NO)
		dialog.action_area.pack_start(buttonNo, True, True, 0)
		buttonOk.connect('clicked', self.result, True, dialog, 'reboot')
		buttonNo.connect('clicked', self.result, False, dialog, 'reboot')
		dialog.show_all()

	# slots
	def _handle_data_changed_in_model(self, begin_idx, end_idx):
		cur_idx = self.listView.selectionModel().currentIndex()
		if not cur_idx.isValid():
			return
		cur_row = cur_idx.row()
		row_range = range(begin_idx.row(), end_idx.row())
		if len(row_range) == 0:
			row_range = [begin_idx.row()]
		if cur_row in row_range:
			self.set_right_frame(cur_idx)

	def _handle_remove_current_action(self, *args):
		print args
		model, cur_idx = self.actSelection.get_selected()
		self.act_model.removeCurrAct(cur_idx)

	def _handle_clean_actions(self, *args):
		print args
		self.act_model.clearRows()

	def _handle_disable_all(self, *args):
		print args
		devs = self.model.disable_all_devices()
		self.disen_device_notif(devs, True)

	def _handle_disable_device(self, *args):
		print args
		model, cur_idx = self.devSelection.get_selected()
		need_id, res = self.model.disable_one_device(cur_idx)
		#print self.devSelection.get_selected_rows()
		self.disen_device_notif(need_id, not res)

	def _handle_exit(self):
		self.hide_all()

	def _handle_action_select_item(self, cur_idx, prev_idx):
		self.actionActionsDelete.setEnabled(cur_idx.isValid())

	def _handle_select_item(self, current_idx, prev_idx):
		self.actionDevicesDisable.setEnabled(current_idx.isValid())
		if not current_idx.isValid():
			return

		if self.model.index_is_hide(current_idx):
			self.actionDevicesDisable.setText(self.tr('&Enable notification'))
		else:
			self.actionDevicesDisable.setText(self.tr('&Disable notification'))
		self.set_right_frame(current_idx)
		

	def _handle_rbb(self, widget, data = ''):
		model, curr_iter = self.devSelection.get_selected()
		if curr_iter is None :
			print 'Device Not selected'
			return
		if data == 'reset' :
			self.set_right_frame(self.model.curr_row(curr_iter))
		elif data == 'accept' :
			self._right_frame_apply(self.model.curr_row(curr_iter))

	def _handle_select_module(self, *args):
		module_iter = self.Detail.modules.get_active_iter()
		if module_iter is None :
			self.Detail.installPacksLabel.set_text('')
			return
		selection_module_name = str(self.Detail.modulesMod.get_value(module_iter, 0))
		#print selection_module_name, '-'
		d = self._current_device()
		if d is None :
			print 'Device not selected'
			return
		print 'Selected : ', d.device_name()
		pkgsi = d.packages_to_install(selection_module_name)
		pkgsr = d.packages_to_remove(selection_module_name)
		detail_html = '<b>For installing this module need:</b>\n'
		if len(pkgsi) > 0:
			detail_html += '\t<i><u>Packages to install:</u></i>\n'
			for p in pkgsi:
				detail_html += '\t\t' + str(p) + '\n'
			detail_html += '\n'
		if len(pkgsr) > 0:
			detail_html += '\t<i><u>Packages to remove:</u></i>\n'
			for p in pkgsr:
				detail_html += '\t\t' + str(p) + '\n'
			detail_html += '\n'

		self.Detail.installPacksLabel.set_markup(detail_html)

	def _handle_apply_actions(self, *args):
		print args
		if self.act_model.pkgs_to_install_exist() or True:
			dialog = gtk.Dialog(title = 'Install akmods too', \
							parent = self.Parent.window, \
							flags = gtk.DIALOG_MODAL, \
							buttons = None)
			label = gtk.Label('Do you have install also akmod (automated kernel module) packages too?')
			dialog.vbox.pack_start(label, True, True, 0)
			buttonOk = gtk.Button(stock = gtk.STOCK_OK)
			dialog.action_area.pack_start(buttonOk, True, True, 0)
			buttonNo = gtk.Button(stock = gtk.STOCK_NO)
			dialog.action_area.pack_start(buttonNo, True, True, 0)
			buttonOk.connect('clicked', self.result, True, dialog, 'act')
			buttonNo.connect('clicked', self.result, False, dialog, 'act')
			dialog.show_all()

	def result(self, widget, answ, dialog, mark):
		dialog.hide_all()
		if answ :
			if mark == 'act' :
				self.Parent.window.set_sensitive(False)
				self._do_act()
				self.Parent.window.set_sensitive(True)
			elif mark == 'reboot' :
				print 'rebooting'

