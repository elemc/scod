#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
from Image import image

class ActionsModel(gtk.ListStore):
	def __init__(self, parent = None):
		gtk.ListStore.__init__(self, str)

		self.Parent = parent

		self.set_column_types(str)
		self._load_imgs()
		self.actions = [] # main data container

	def _load_imgs(self):
		self.gears_icon = gtk.Image()
		self.gears_icon.set_from_pixbuf(image("../img/gears.svg"))

	def add_new_action(self, devid, name, pkgs = [], atype=0):
		ad = {}
		ad['devid']	  = devid
		ad['name']	  = name
		ad['type']	  = atype
		ad['pkgs']	  = pkgs
		self.actions.append(ad)
		## выяснить результат действия по сигналу
		#self.dataChanged.emit(self.index(len(self.actions)-1, 0),self.index(len(self.actions)-1, 0))
		self.append([name])
		#self.connect("columns-changed", self.Parent._handle_data_changed_in_model)

	def del_action(self, *args):
		pass
