#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from Image import *

def addModule(mod, text):
	mod.append_text(text)

def entryText(entry, text):
	entry.set_text(text)

def addNote(obj, text):
	obj.set_text(text)
	obj.show()

separator = gtk.HSeparator()

nameLabel = gtk.Label()
nameLabel.set_text('Name :')
nameLabel.set_justify(gtk.JUSTIFY_LEFT)
nameLabel.set_alignment(0.0, 0.0)
entry = gtk.Entry(max = 0)
entry.set_editable(False)
entry.set_visibility(True)
selectModuleLabel = gtk.Label()
selectModuleLabel.set_text('Select Module :')
selectModuleLabel.set_justify(gtk.JUSTIFY_LEFT)
selectModuleLabel.set_alignment(0.0, 0.0)
modules = gtk.ComboBox()
actionDeviceLabel = gtk.Label()
actionDeviceLabel.set_text('Action Device :')
actionDeviceLabel.set_justify(gtk.JUSTIFY_LEFT)
actionDeviceLabel.set_alignment(0.0, 0.0)
neededActionLabel = gtk.Label()
neededActionLabel.set_text('For installing this module need :')
neededActionLabel.set_justify(gtk.JUSTIFY_LEFT)
neededActionLabel.set_alignment(0.0, 0.0)
installPacksLabel = gtk.Label()
installPacksLabel.set_text('Packages to install :')
installPacksLabel.set_justify(gtk.JUSTIFY_LEFT)
installPacksLabel.set_alignment(0.0, 0.0)

reset = gtk.Button('Reset')
reset.set_alignment(0.0, 0.0)
reset.set_image(reset_)
accept = gtk.Button('Accept')
accept.set_alignment(1.0, 1.0)
accept.set_image(accept_)

hbox = gtk.HBox(False, 1)
hbox.pack_start(reset, False, True, 0)
hbox.pack_end(accept, False, True, 0)
reset.show()
accept.show()

Detail = gtk.VBox(False, 1)
Detail.set_border_width(1)

Detail.pack_start(nameLabel, False, False, 0)
Detail.pack_start(entry,  False, False, 0)
Detail.pack_start(selectModuleLabel, False, False, 0)
Detail.pack_start(modules, False, False, 0)
Detail.pack_start(actionDeviceLabel, False, False, 0)
Detail.pack_start(neededActionLabel, False, False, 0)
Detail.pack_start(installPacksLabel, False, False, 0)
Detail.pack_start(separator, False, True, 0)
Detail.pack_start(hbox, False, True, 0)
separator.show()
actionDeviceLabel.show()
neededActionLabel.show()
installPacksLabel.show()
selectModuleLabel.show()
modules.show()
entry.show()
hbox.show()
nameLabel.show()
