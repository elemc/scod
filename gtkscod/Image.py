#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

def imag(name):
	return gtk.gdk.pixbuf_new_from_file_at_size(name, 30, 30)

disable = gtk.Image()
disable.set_from_pixbuf(imag('../img/disable.png'))
disable.show()

disableall = gtk.Image()
disableall.set_from_pixbuf(imag('../img/disableall.png'))
disableall.show()
reset_ = gtk.Image()
reset_.set_from_pixbuf(imag('../img/disableall.png'))
reset_.show()

deleteaction = gtk.Image()
deleteaction.set_from_pixbuf(imag('../img/deleteaction.png'))
deleteaction.show()

cancelaction = gtk.Image()
cancelaction.set_from_pixbuf(imag('../img/cancelactions.png'))
cancelaction.show()

apply_ = gtk.Image()
apply_.set_from_pixbuf(imag('../img/apply.png'))
apply_.show()
accept_ = gtk.Image()
accept_.set_from_pixbuf(imag('../img/apply.png'))
accept_.show()
