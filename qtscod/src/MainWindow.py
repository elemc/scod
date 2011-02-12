#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow
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
		#self.model.reset()

	def _init_menu(self):
		self.actionFileExit.triggered.connect(self._handle_exit)

	# Slots
	def _handle_exit(self):
		self.hide()

	def add_new_device(self, dev): #FIXME: add object Device
		self.model.add_new_device(dev)
		self.show_notification()

	def show_notification(self):
		if self.isHidden():
			self.show()

	def start_listen(self):
		self.lt.start()
