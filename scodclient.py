# Simple console SCOD client

import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop

def new_device(dev_id, dev_name, modules, dev_type):
	print "Device: %s (%s) \t %s" % (dev_name, dev_type, dev_id)
	for m in modules:
		print "\t * %s" % m

DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
scod = bus.get_object('ru.russianfedora.SCOD', '/ru/russianfedora/SCOD')
iface = dbus.Interface(scod, dbus_interface='ru.russianfedora.SCOD')
iface.connect_to_signal('new_device', new_device)
gobject.MainLoop().run()
