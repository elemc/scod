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
		#self._load_imgs()
		self.data_list = []
		self.items = []

	def _load_imgs(self):
		#self.gears_icon = gtk.Image()
		#self.gears_icon.set_from_pixbuf(image("../img/gears.svg"))
		self.image = image("../img/gears.svg")

	def add_new_device(self, dev):
		d = Device(dev)
		self.data_list.append(d)
		print "Device added: %s (%s)" % (d.device_name(), d.device_type())
		item = self.append([dev['name'], gtk.STOCK_PREFERENCES])
		#item = self.append([dev['name'], gtk.STOCK_ADD])
		self.items.append(item)

	def device_by_index(self, cur_idx):
		pass
