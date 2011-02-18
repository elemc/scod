#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import QSize,QString
from PyQt4.QtGui import QMainWindow, QMessageBox, QDialogButtonBox
from ui.MainWindow import Ui_MainWindow

from src.ListenThread import ListenThread
from src.DevicesListModel import DevicesListModel
from src.ActionsModel import ActionsModel

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self._init_menu()
		self._init_models()
		self.lt = ListenThread(self.add_new_device)
		
		# right frame
		self.comboBoxModules.currentIndexChanged.connect(self._handle_select_module)
		self.buttonBoxDetails.clicked.connect(self._handle_rbb)

	def _init_menu(self):
		self.actionFileExit.triggered.connect(self._handle_exit)
	
	def _init_models(self):
		self.model = DevicesListModel(self)
		self.listView.setModel(self.model)
		self.listView.selectionModel().currentChanged.connect(self._handle_select_item)

		self.act_model = ActionsModel(self)
		self.listViewActions.setModel(self.act_model)
	
	def add_new_device(self, dev): 
		self.model.add_new_device(dev)
		self.show_notification()

	def show_notification(self):
		if self.isHidden():
			self.show()

	def start_listen(self):
		self.lt.start()

	def _right_frame_apply(self, idx):
		d = self.model.device_by_index(idx)
		sel_cb_idx = self.comboBoxModules.currentIndex()
		sel_module = str(self.comboBoxModules.itemData(sel_cb_idx).toString())
		pkgsi = d.packages_to_install(sel_module)
		pkgsr = d.packages_to_remove(sel_module)
		# TODO: make a actions for device
		if len(pkgsi) > 0:
			self.act_model.add_new_action(sel_module, pkgsi, 0)
		if len(pkgsr) > 0:	
			rem_mds = str(', ').join(d.device_modules(sel_module))
			self.act_model.add_new_action(rem_mds, pkgsr, 1)
		
	
	def _current_device(self, idx = None):
		cur_idx = idx
		if idx is None:
			cur_idx = self.listView.selectionModel().currentIndex()
		return self.model.device_by_index(cur_idx)

	def set_right_frame(self, idx):
		self.comboBoxModules.clear()
		d = self._current_device(idx)
		curdrv = QString()
		if d.current_driver() is None or len(d.current_driver()) == 0:
			curdrv = self.tr('Not installed')
		else:
			curdrv = QString('- %s -' % d.current_driver())
		self.comboBoxModules.addItem(curdrv, QString(d.current_driver()))

		self.lineEditName.setText(d.device_name())
		for m in d.device_modules():
			devmod = QString()
			if m == d.current_driver():
				continue
			else:
				devmod = QString('%s' % m)
			self.comboBoxModules.addItem(devmod, QString(m))

	# slots
	def _handle_exit(self):
		self.hide()

	def _handle_select_item(self, current_idx, prev_idx):
		if not current_idx.isValid():
			return
		self.set_right_frame(current_idx)

	def _handle_rbb(self, but):
		cur_idx = self.listView.selectionModel().currentIndex()
		if self.buttonBoxDetails.buttonRole(but) == QDialogButtonBox.ResetRole:
			self.set_right_frame(cur_idx)
		elif self.buttonBoxDetails.buttonRole(but) == QDialogButtonBox.ApplyRole:
			self._right_frame_apply(cur_idx)


	def _handle_select_module(self, module_index):
		if module_index == -1:
			self.labelDetails.setText('')
			return
		selection_module_name = str(self.comboBoxModules.itemData(module_index).toString())
		print "Module changed at pos %s - %s" % (module_index, selection_module_name)
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
