#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ================================= #
# Python script                     #
# Author: Alexei Panov              #
# e-mail: elemc AT atisserv DOT ru  #
# ================================= #

from dbus.mainloop.qt import DBusQtMainLoop
from PackageKit import PackageKit, PackageKitTransaction
from PyQt4.QtCore import QThread,QEventLoop

class PackageKitTransactionQt(PackageKitTransaction):
    def __init__(self, tctrl, tid, main_loop):
        PackageKitTransaction.__init__(self, tctrl, tid, main_loop)

    def _start(self):
        self._is_started = True
        #QEventLoop().exec_()
        self.main_loop.exec_()

    def _stop(self):
        self._is_started = False
        #QEventLoop().exit()
        self.main_loop.exit()

class PackageKitQt(PackageKit):
    def __init__(self, main_loop = None):
        PackageKit.__init__(self, main_loop)

    def _get_transaction_ptr(self, tctrl, tid, dbus_loop):
        trans = PackageKitTransactionQt(tctrl, tid, dbus_loop)
        return trans
        
    def _init_empty_loop(self, main_loop):
        if main_loop is None:
            main_loop = QEventLoop() #DBusQtMainLoop()
        return main_loop
