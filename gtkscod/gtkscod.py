#!/usr/bin/env python

import sys
try:
	import pygtk
	pygtk.require("2.0")
except:
	pass
	
try:
	import gtk
	import gtk.glade
except:
	sys.exit(1)

from pymainwindow import GTKScodMainWindow

if __name__ == '__main__':
	app = GTKScodMainWindow()
	gtk.main()

