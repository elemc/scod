#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

def image(name):
	return gtk.gdk.pixbuf_new_from_file_at_size(name, 30, 30)

disable = gtk.Image()
#disable.set_from_pixbuf(image('../img/disable.png'))
disable.set_from_stock(gtk.STOCK_JUMP_TO, 30)
disable.show()

disableall = gtk.Image()
disableall.set_from_stock(gtk.STOCK_DISCONNECT, 30)
disableall.show()
reset_ = gtk.Image()
reset_.set_from_pixbuf(image('../img/disableall.png'))
reset_.show()

deleteaction = gtk.Image()
deleteaction.set_from_pixbuf(image('../img/deleteaction.png'))
deleteaction.show()

cancelaction = gtk.Image()
cancelaction.set_from_pixbuf(image('../img/cancelactions.png'))
cancelaction.show()

apply_ = gtk.Image()
apply_.set_from_pixbuf(image('../img/apply.png'))
apply_.show()
accept_ = gtk.Image()
accept_.set_from_pixbuf(image('../img/apply.png'))
accept_.show()

enableall = gtk.Image()
enableall.set_from_stock(gtk.STOCK_CONNECT, 30)
enableall.show()
