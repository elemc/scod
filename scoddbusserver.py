# Python class for DBUS daemon

import dbus
import dbus.service
import gobject
from dbus.mainloop.glib import DBusGMainLoop, threads_init
from threading import Thread
import time
import os, os.path
from scodcache import SCODCache

global_service_name = 'ru.russianfedora.SCOD'
global_service_path = '/ru/russianfedora/SCOD'

class SCODDBUSServer(dbus.service.Object):
    def __init__(self):
        name = dbus.service.BusName(global_service_name, dbus.SystemBus())
        dbus.service.Object.__init__(self, name, global_service_path)
        self.devices = {}

    def _dbus_array_to_list(self, da):
        ret_res = []
        for ds in da:
            ret_res.append(str(ds))
        return ret_res

    @dbus.service.method(dbus_interface=global_service_name, in_signature='as', out_signature='b')  
    def disableDeviceNotification(self, dev_id):
        sc = SCODCache()
        return sc.add_to_ddn(self._dbus_array_to_list(dev_id))
    
    @dbus.service.method(dbus_interface=global_service_name, in_signature='s', out_signature='b')
    def enableDeviceNotification(self, dev_id):
        sc = SCODCache()
        return sc.del_from_ddn(dev_id)

    @dbus.service.signal(dbus_interface=global_service_name, signature='sss') #signature='ssass')
    def new_device(self, dev_id, dev_name, dev_type):
        pass

    @dbus.service.method(dbus_interface=global_service_name, in_signature='s', out_signature='s')
    def deviceName(self, dev_id):
        res = self.get_param(dev_id, 'name')
        if res is None:
            return ""
        return res
    
    @dbus.service.method(dbus_interface=global_service_name, in_signature='s', out_signature='as')
    def deviceModules(self, dev_id):
        m = self.get_param(dev_id, 'modules')
        if m is None:
            return []
        return m.keys()
    
    @dbus.service.method(dbus_interface=global_service_name, in_signature='ss', out_signature='as')
    def packagesForModule(self, dev_id, module_name):
        m = self.get_param(dev_id, 'modules')
        if m is not None:
            if module_name in m.keys():
                return m[module_name]
        return []

    @dbus.service.method(dbus_interface=global_service_name, in_signature='s', out_signature='b')
    def disableDeviceNotif(self, dev_id):
        pass
        # this is method desabled device notification in the future

    @dbus.service.method(dbus_interface=global_service_name, in_signature='s', out_signature='s')
    def currentDriver(self, dev_id):
        res = self.get_param(dev_id, 'driver')
        if res is None:
            return ""
        return res

    @dbus.service.method(dbus_interface=global_service_name, in_signature='', out_signature='')
    def listDevices(self):
        for dev_id in self.devices.keys():
            dev = self.devices[dev_id]
            self.new_device(dev_id, dev['name'], dev['type'])

    # control methods
    def listen(self):
        gobject.MainLoop().run()

    def stop(self):
        gobject.MainLoop().quit()

    def get_param(self, dev_id, param_name):
        if dev_id in self.devices.keys():
            dev = self.devices[dev_id]
            if param_name in dev.keys():
                return dev[param_name]

        return None

    def tell_about_new_device(self, scoddev):
        dev = {}
        dev['name']     = scoddev.dev_name
        dev['modules']  = scoddev.dev_modules
        dev['type']     = scoddev.dev_type
        dev['driver']   = scoddev.dev_driver
        self.devices[scoddev.dev_id] = dev

        self.new_device(scoddev.dev_id, scoddev.dev_name, scoddev.dev_type)

class DBUSThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        gobject.threads_init()
        DBusGMainLoop(set_as_default=True)
        self.dbus_server    = SCODDBUSServer()

    def run(self):
        self.dbus_server.listen()
    
    def stop(self):
        self.dbus_server.stop()

    def tell_about_new_device(self, dev):
        self.dbus_server.tell_about_new_device(dev)
        print "Device: %s" % dev.dev_name

