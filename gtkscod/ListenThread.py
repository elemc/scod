#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread

# dbus
from dbus.mainloop.glib import DBusGMainLoop
import dbus
import gobject

class ListenThread(Thread):
	def __init__(self, mainloop = None, parent_class = None):
		Thread.__init__(self)
		if mainloop is None :
			self.main_loop = gobject.MainLoop()
		else :
			self.main_loop = mainloop
		DBusGMainLoop(set_as_default = True)

		self.mw					= parent_class
		bus						= dbus.SystemBus()
		try:
			self.scod			= bus.get_object('ru.russianfedora.SCOD', '/ru/russianfedora/SCOD')
			self.iface_signal	= dbus.Interface(self.scod, dbus_interface='ru.russianfedora.SCOD')
			self.iface_cmd		= dbus.Interface(self.scod, dbus_interface='ru.russianfedora.SCOD')
		except:
			print 'init error'
			self.mw				= None
			self.iface_signal	= None
			self.iface_cmd		= None
			self.scod			= None
			return

		self.mw = parent_class

	def run(self):
		if (self.iface_signal is None) or (self.iface_cmd is None):
			print ' error'
			return
		self.iface_signal.connect_to_signal('new_device', self.new_device_handler)
		self.iface_cmd.listDevices()
		print 'thread start'
		self.main_loop.run()
	
	def stop(self):
		self.main_loop.quit()

	def disable_device_notif(self, dev_id):
		dest = []
		if type(dev_id) is str:
			dest.append(dev_id)
		elif type(dev_id) is list:
			dest = dev_id
		else:
			dest.append(str(dev_id))
		res = self.iface_cmd.disableDeviceNotification(dest)
		if not res:
			print "Error in disableDeviceNotification"

	def enable_device_notif(self, dev_id):
		res = self.iface_cmd.enableDeviceNotification(dev_id)
		if not res:
			print "Error in enableDeviceNotification"

	def new_device_handler(self, dev_id, dev_name, dev_type):
		if self.mw is None:
			return
		device_dict = {}
		m = {}
		modules = self.iface_cmd.deviceModules(dev_id)
		for mod in modules:
			pkgs = self.iface_cmd.packagesForModule(dev_id, mod)
			m[mod] = pkgs
		cur_drv = self.iface_cmd.currentDriver(dev_id)

		device_dict['id']				= dev_id
		device_dict['name']				= dev_name
		device_dict['type']				= dev_type
		device_dict['modules']			= m
		device_dict['current_driver']	= cur_drv

		self.mw(device_dict)


if __name__ == "__main__":
	try :
		main_loop = gobject.MainLoop()
		trd = ListenThread(main_loop)
		trd.start()
	except KeyboardInterrupt :
		print 'tread closed manually'
		trd.stop()
