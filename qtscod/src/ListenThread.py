#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread

# dbus
from dbus.mainloop.glib import DBusGMainLoop
import dbus
import gobject

class ListenThread(Thread):
	def __init__(self, parent_class):
		Thread.__init__(self)
		gobject.threads_init()	
		DBusGMainLoop(set_as_default=True)

		#self.window_class	= parent_class
		self.mw				= parent_class
		bus					= dbus.SessionBus()
		try:
			self.scod			= bus.get_object('ru.russianfedora.SCOD', '/ru/russianfedora/SCOD')
			self.iface_signal	= dbus.Interface(self.scod, dbus_interface='ru.russianfedora.SCOD')
			self.iface_cmd		= dbus.Interface(self.scod, dbus_interface='ru.russianfedora.SCOD')
		except:
			self.mw				= None
			self.iface_signal	= None
			self.iface_cmd		= None
			self.scod			= None
			return
		
		#self.mw = parent_class

	def run(self):
		if (self.iface_signal is None) or (self.iface_cmd is None):
			return
		self.iface_signal.connect_to_signal('new_device', self.new_device_handler)
		self.iface_cmd.listDevices()
		gobject.MainLoop().run()
	
	def stop(self):
		gobject.MainLoop().quit()

	def request_device(self, dev_id):
		pass	

	def new_device_handler(self, dev_id, dev_name, dev_type):
		if self.mw is None:
			return
			#self.mw = self.window_class() 

		self.mw.add_new_device() #FIXME
		#if not self.mw.isShowned():
		self.mw.show_notification()
