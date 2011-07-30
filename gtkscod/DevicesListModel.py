#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
from Image import image
from Device import Device

class DevicesListModel(gtk.ListStore):
	def __init__(self, parent = None):
		gtk.ListStore.__init__(self, str)

		self.set_column_types(str, str)
		self.data_list = []

	def add_new_device(self, dev):
		d = Device(dev)
		self.data_list.append(d)
		print "Device added: %s (%s)" % (d.device_name(), d.device_type())
		item = self.append([dev['name'], gtk.STOCK_PREFERENCES])
		#item = self.append([dev['name'], gtk.STOCK_ADD])

	def device_by_index(self, cur_idx):
		if cur_idx == -1 :
			return None
		return self.data_list[cur_idx]
