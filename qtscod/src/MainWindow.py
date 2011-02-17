#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import QSize,QString
from PyQt4.QtGui import QMainWindow, QMessageBox, QDialogButtonBox
#from PyQt4.QtCore.Qt import tr
from ui.MainWindow import Ui_MainWindow

from src.ListenThread import ListenThread
from src.DevicesListModel import DevicesListModel

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self._init_menu()
		self.lt = ListenThread(self.add_new_device)
		self.model = DevicesListModel(self)
		self.listView.setModel(self.model)
		self.listView.selectionModel().currentChanged.connect(self._handle_select_item)
		#self._right_frame_modif = False
		#self.comboBoxModules.currentIndexChanged.connect(self._handle_select_module)
		self.buttonBoxDetails.clicked.connect(self._handle_rbb)

	def _init_menu(self):
		self.actionFileExit.triggered.connect(self._handle_exit)

	def add_new_device(self, dev): #FIXME: add object Device
		self.model.add_new_device(dev)
		self.show_notification()

	def show_notification(self):
		if self.isHidden():
			self.show()

	def start_listen(self):
		self.lt.start()

	def _right_frame_apply(self, idx):
		d = self.model.device_by_index(idx)
		# TODO: make a actions for device
	
	def set_right_frame(self, idx):
		#print "Changed row: %s, column %s" % (idx.row(), idx.column())
		#if self._right_frame_modif:
		#	result = QMessageBox.question(self, self.tr('Reset changes'), 
		#				self.tr('You not applying changes. Apply it?'), QMessageBox.Yes and QMessageBox.No, QMessageBox.Yes)
		#	if result == QMessageBox.Yes:
		#		self._right_frame_apply()

		self.comboBoxModules.clear()
		#self._right_frame_modif = False
		
		d = self.model.device_by_index(idx)
		curdrv = QString()
		if d.current_driver() is None or len(d.current_driver()) == 0:
			curdrv = self.tr('Not installed')
		else:
			curdrv = QString('- %s -' % d.current_driver())
		self.comboBoxModules.addItem(curdrv, d.current_driver())

		self.lineEditName.setText(d.device_name())
		for m in d.device_modules():
			devmod = QString()
			if m == d.current_driver():
				continue
			else:
				devmod = QString('%s' % m)
			self.comboBoxModules.addItem(devmod, m)

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
			self._right_frame_apply()


	#def _handle_select_module(self, module_index):
		#selection_module_name = self.comboBoxModules.itemText(module_index)
		#print "Module changed %s" % selection_module_name
		#self._right_frame_modif = True
