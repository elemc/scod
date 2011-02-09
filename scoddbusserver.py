# Python class for DBUS daemon

import dbus
import dbus.service
import gobject
from dbus.mainloop.glib import DBusGMainLoop, threads_init
from threading import Thread
import time

global_service_name = 'ru.russianfedora.SCOD'
global_service_path = '/ru/russianfedora/SCOD'

class SCODDBUSServer(dbus.service.Object):
	def __init__(self):
		name = dbus.service.BusName(global_service_name, dbus.SessionBus())
		dbus.service.Object.__init__(self, name, global_service_path)
		#gobject.threads_init()
		#threads_init()
			
	@dbus.service.signal(dbus_interface=global_service_name, signature='ssass')
	def new_device(self, dev_id, dev_name, dev_modules, dev_type):
		pass

	@dbus.service.method(dbus_interface=global_service_name, in_signature='s', out_signature='b')
	def disableDeviceNotif(self, did):
		pass
		# this is method desabled device notification in the future

	@dbus.service.method(dbus_interface=global_service_name, in_signature='', out_signature='as')
	def listDevices(self):
		devs = []
		return devs

	def listen(self):
		gobject.MainLoop().run()

	def stop(self):
		gobject.MainLoop().quit()

	def tell_about_new_device(self, scoddev):
		dev_id 		= scoddev.dev_id		# s
		dev_name	= scoddev.dev_name		# s
		dev_modules	= scoddev.dev_modules	# as
		dev_type	= scoddev.dev_type		# s
		self.new_device(dev_id, dev_name, dev_modules, dev_type)

class DBUSThread(Thread):
	def __init__(self):
		Thread.__init__(self)
		gobject.threads_init()
		#threads_init()
		DBusGMainLoop(set_as_default=True)
		self.dbus_server	= SCODDBUSServer()

	def run(self):
		self.dbus_server.listen()
	
	def stop(self):
		self.dbus_server.stop()

	def tell_about_new_device(self, dev):
		self.dbus_server.tell_about_new_device(dev)
		print "Device: %s" % dev.dev_name

