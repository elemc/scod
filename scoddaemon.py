# Python daemon class

import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop, threads_init

from pyudev import Context, Monitor
from scoddbusserver import DBUSThread, SCODDBUSServer
from scoddevice import SCODDevice
import time

class SCODDaemon:
	def __init__(self):
		self.context = Context()
		self.monitor = None
		
		self.dbus = DBUSThread()
		self.dbus.start()
		self.tell_about_devices()
		print "Done."

	def __del__(self):
		self.dbus.stop()

	def start_listen(self):
		self.monitor = Monitor.from_netlink(self.context)
		for action, device in self.monitor:
			self._new_device(action, device)

	def _new_device(self, act, dev):
		if act != 'add':
			return
	
		time.sleep(0.1)
		if ('MODALIAS' not in dev.keys()): # and ( 'modalias' not in dev.attributes.keys()  ):
			return

		d = SCODDevice(dev)
		if ( d.isOurDevice() ):
			self.dbus.tell_about_new_device(d)
	
	def tell_about_devices(self):
		print "DBUS is %s" % self.dbus.isAlive()
		for dev in self.context.list_devices():
			d = SCODDevice(dev)
			if ( d.isOurDevice() ):
				self.dbus.tell_about_new_device(d)
	def stop(self):
		self.dbus.stop()
