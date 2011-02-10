#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow
from ui.MainWindow import Ui_MainWindow

from src.ListenThread import ListenThread

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self._init_menu()
		self.lt = ListenThread(self)
		#self.lt.start()

	def _init_menu(self):
		self.actionFileExit.triggered.connect(self._handle_exit)

	# Slots
	def _handle_exit(self):
		self.hide()

	def add_new_device(self): #FIXME: add object Device
		pass


	def show_notification(self):
		if self.isHidden():
			self.show()

	def start_listen(self):
		self.lt.start()
