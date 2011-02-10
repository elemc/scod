# Simple console SCOD client

import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop

def new_device(dev_id, dev_name, dev_type):
	iface_cl = dbus.Interface(scod, dbus_interface='ru.russianfedora.SCOD')
	print "Device: %s (%s) \t %s" % (dev_name, dev_type, dev_id)
	modules = iface_cl.deviceModules(dev_id)
	for m in modules:
		print "\t * %s" % m
		pkgs = iface_cl.packagesForModule(dev_id, m)
		for p in pkgs:
			print "\t\t + %s" % p

DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
scod = bus.get_object('ru.russianfedora.SCOD', '/ru/russianfedora/SCOD')
iface = dbus.Interface(scod, dbus_interface='ru.russianfedora.SCOD')
iface.connect_to_signal('new_device', new_device)
iface.listDevices()

gobject.MainLoop().run()
