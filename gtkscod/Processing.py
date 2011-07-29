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
		#self._init_menu()
		self.lt = ListenThread(parent_class = self.add_new_device)
		self._install_akmods = False
		self._main_pko = None #PackageKitClient()
		
		# right frame
		#self.comboBoxModules.currentIndexChanged.connect(self._handle_select_module)
		self.Detail.reset.connect('clicked', self._handle_rbb, 'reset')
		self.Detail.accept.connect('clicked', self._handle_rbb, 'accept')

	def closeEvent(self, event):
		event.ignore()
		self.hide()

	def _init_menu(self):
		self.actionFileExit.triggered.connect(self._handle_exit)
		
		self.listView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.listViewActions.setContextMenuPolicy(Qt.ActionsContextMenu)

		# context menu for listView
		for act in self.menuDevices.actions():
			self.listView.addAction(act)
		# context menu for listViewActions
		for act in self.menuActions.actions():
			self.listViewActions.addAction(act)

	def _init_models(self):
		self.listView = self.Parent.listDev
		self.model = DevicesListModel(self)
		self.listView.set_model(self.model)
		self.devSelection = self.listView.get_selection()
		self.devSelection.set_mode(gtk.SELECTION_BROWSE)
		#self.listView.selectionModel().currentChanged.connect(self._handle_select_item)
		self.listView.connect("columns-changed", self._handle_data_changed_in_model)

		self.listViewActions = self.Parent.listAct
		self.act_model = ActionsModel(self)
		self.listViewActions.set_model(self.act_model)
		self.actSelection = self.listViewActions.get_selection()
		self.actSelection.set_mode(gtk.SELECTION_BROWSE)
		#self.listViewActions.selectionModel().currentChanged.connect(self._handle_action_select_item)
		self.listViewActions.connect("columns-changed", self._handle_action_select_item)

		#self.act_model.actionDeleted.connect(self.model.reset_changes)
		#self.model.dataChanged.connect(self._handle_data_changed_in_model)

	def _init_pk(self):
		if self._main_pko is None:
			self._main_pko = PackageKitClient()

	def add_new_device(self, dev):
		#print dev
		self.Detail.entry.set_text(dev['name'])
		self.model.add_new_device(dev)
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
		sel_cb_idx = self.comboBoxModules.currentIndex()
		sel_module = str(self.comboBoxModules.itemData(sel_cb_idx).toString())
		if sel_module == d.current_driver():
			return
		
		self.act_model.remove_actions_by_devid(d.device_id(), sel_module)
		pkgsi = d.packages_to_install(sel_module)
		pkgsr = d.packages_to_remove(sel_module)
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
			model, cur_idx = self.devSelection.get_selected()
		return self.model.device_by_index(cur_idx)

	def set_right_frame(self, idx):
		self.Detail.modules.clear()
		d = self._current_device(idx)
		curdrv = QString()
		if d.current_driver() is None or len(d.current_driver()) == 0:
			curdrv = self.tr('Not installed')
		else:
			curdrv = QString('- %s -' % d.current_driver())
		self.comboBoxModules.addItem(curdrv, QString(d.current_driver()))

		self.lineEditName.setText(d.device_name())
		our_sel_idx = -1
		for m in d.device_modules():
			devmod = QString()
			if m == d.current_driver():
				continue
			elif m == d.selected_driver():
				devmod = QString('* %s *' % m)
				our_sel_idx = self.comboBoxModules.count()
			else:
				devmod = QString('%s' % m)
			self.comboBoxModules.addItem(devmod, QString(m))

		if our_sel_idx != -1:
			self.comboBoxModules.setCurrentIndex(our_sel_idx)

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
		res = QMessageBox.question(self, 
				   self.tr("Operations done"), 
				   self.tr("All operations applied. You may reboot a system. Reboot now?"),
				   QMessageBox.Yes and QMessageBox.No, QMessageBox.Yes)
		if res == QMessageBox.Yes:
			print 'rebooting'
					   
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
		#cur_idx = self.listViewActions.selectionModel().currentIndex()
		#self.act_model.removeRows(cur_idx.row(), 1)

	def _handle_clean_actions(self, *args):
		print args
		#self.act_model.clearRows()

	def _handle_disable_all(self, *args):
		print args
		#devs = self.model.disable_all_devices()
		#self.disen_device_notif(devs, True)

	def _handle_disable_device(self, *args):
		print args
		#cur_idx = self.listView.selectionModel().currentIndex()
		#this_is_hide_item = self.model.index_is_hide(cur_idx)
		#need_id = self.model.index_hide(cur_idx, not this_is_hide_item)
		#self._handle_select_item(cur_idx, cur_idx)
		
		#self.disen_device_notif(need_id, not this_is_hide_item)

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
		#(model, iter) = treeselection.get_selected()
		model, cur_idx = self.devSelection.get_selected()
		if data == 'reset' :
			self.set_right_frame(cur_idx)
		elif data == 'accept' :
			self._right_frame_apply(cur_idx)

	def _handle_select_module(self, module_index):
		if module_index == -1:
			self.labelDetails.setText('')
			return
		selection_module_name = str(self.comboBoxModules.itemData(module_index).toString())
		d = self._current_device()
		pkgsi = d.packages_to_install(selection_module_name)
		pkgsr = d.packages_to_remove(selection_module_name)
		detail_html = QString('<h4>%1 </h4>').arg(self.tr('For installing this module need:'))
		if len(pkgsi) > 0:
			detail_html += QString('<p>%1 <ul>').arg(self.tr('Packages to install:'))
			for p in pkgsi:
				detail_html += QString('<li>%1</li>').arg(p)
			detail_html += QString('</ul></p>')
		if len(pkgsr) > 0:
			detail_html += QString('<p>%1 <ul>').arg(self.tr('Packages to remove: '))
			for p in pkgsr:
				detail_html += QString('<li>%1</li>').arg(p)
			detail_html += QString('</ul></p>')

		self.labelDetails.setText(detail_html)

	def _handle_apply_actions(self, *args):
		print args
		"""if self.act_model.pkgs_to_install_exist():
			result = QMessageBox.question(self, self.tr('Install akmods too'), 
						  self.tr('Do you have install also akmod (automated kernel module) packages too?'),
						  QMessageBox.Yes and QMessageBox.No, QMessageBox.Yes)
			if result == QMessageBox.Yes:
				self._install_akmods = True
		
		self.setEnabled(False)
		self._do_act()
		self.setEnabled(True)"""

