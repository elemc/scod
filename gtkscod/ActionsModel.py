#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
from Image import image

class ActionsModel(gtk.ListStore):
	def __init__(self, parent = None):
		gtk.ListStore.__init__(self)

		self.set_column_types('gboolean', str)
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
		#self.dataChanged.emit(self.index(len(self.actions)-1, 0),self.index(len(self.actions)-1, 0))
		## выяснить назначение сигнала
		self.append([state, act])
