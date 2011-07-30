#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
from Image import *

class Detail(gtk.VBox):
	def __init__(self, p1, p2, parent = None):
		gtk.VBox.__init__(self, p1, p2)

		self.set_border_width(1)

		self.separator = gtk.HSeparator()

		self.nameLabel = gtk.Label()
		self.nameLabel.set_text('Name :')
		self.nameLabel.set_justify(gtk.JUSTIFY_LEFT)
		self.nameLabel.set_alignment(0.0, 0.0)

		self.entry = gtk.Entry(max = 0)
		self.entry.set_editable(False)
		self.entry.set_visibility(True)

		self.selectModuleLabel = gtk.Label()
		self.selectModuleLabel.set_text('Select Module :')
		self.selectModuleLabel.set_justify(gtk.JUSTIFY_LEFT)
		self.selectModuleLabel.set_alignment(0.0, 0.0)

		self.modulesMod = gtk.ListStore(str)
		self.modules = gtk.ComboBox(self.modulesMod)
		cell = gtk.CellRendererText()
		self.modules.pack_start(cell, True)
		self.modules.add_attribute(cell, 'text', 0)

		self.actionDeviceLabel = gtk.Label()
		self.actionDeviceLabel.set_text('Action Device :')
		self.actionDeviceLabel.set_justify(gtk.JUSTIFY_LEFT)
		self.actionDeviceLabel.set_alignment(0.0, 0.0)

		self.neededActionLabel = gtk.Label()
		#self.neededActionLabel.set_text('For installing this module need :')
		self.neededActionLabel.set_justify(gtk.JUSTIFY_LEFT)
		self.neededActionLabel.set_alignment(0.0, 0.0)

		self.installPacksLabel = gtk.Label()
		self.installPacksLabel.set_text('Packages to install :')
		self.installPacksLabel.set_justify(gtk.JUSTIFY_LEFT)
		self.installPacksLabel.set_alignment(0.0, 0.0)

		self.reset = gtk.Button('Reset')
		self.reset.set_alignment(0.0, 0.0)
		self.reset.set_image(reset_)
		self.accept = gtk.Button('Accept')
		self.accept.set_alignment(1.0, 1.0)
		self.accept.set_image(accept_)

		self.hbox = gtk.HBox(False, 1)
		self.hbox.pack_start(self.reset, False, True, 0)
		self.hbox.pack_end(self.accept, False, True, 0)

		self.pack_start(self.nameLabel, False, False, 0)
		self.pack_start(self.entry,  False, False, 0)
		self.pack_start(self.selectModuleLabel, False, False, 0)
		self.pack_start(self.modules, False, False, 0)
		self.pack_start(self.actionDeviceLabel, False, False, 0)
		self.pack_start(self.neededActionLabel, False, False, 0)
		self.pack_start(self.installPacksLabel, False, False, 0)
		self.pack_start(self.separator, False, True, 0)
		self.pack_start(self.hbox, False, True, 0)

	def addModule(self, mod, text):
		mod.append_text(text)

	def entryText(self, entry, text):
		entry.set_text(text)

	def addNote(self, obj, text):
		obj.set_text(text)
		#obj.show()
