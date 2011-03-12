#!/usr/bin/env python

import pygtk
import gtk, gtk.glade

class GTKScodMainWindow:
    def __init__(self):
        self.gladefile = 'mainwindow.glade'
        self.glade_project = gtk.glade.XML(self.gladefile)
        self.window = self.glade_project.get_widget("main_window")
        if self.window:
            self.window.connect('destroy', gtk.main_quit)
	
