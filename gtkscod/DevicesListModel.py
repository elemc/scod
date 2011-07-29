#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
from Image import image
from Device import Device

class DevicesListModel(gtk.ListStore):
	def __init__(self, parent = None):
		gtk.ListStore.__init__(self)

		self.set_column_types('gboolean', str)
