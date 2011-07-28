#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
from Detail import Detail
from Image import *
from ListenThread import ListenThread
from Processing import WindowProcessing

class gtkScodClient:
	# Obligatory basic callback
	def print_hello(self, w, data):
		print "Hello, World!"

	def get_main_menu(self, window):
		accel_group = gtk.AccelGroup()
		item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
		item_factory.create_items(self.menu_items)
		window.add_accel_group(accel_group)
		self.item_factory = item_factory
		return item_factory.get_widget("<main>")

	def _quit(self, *args):
		#print args
		self.listen_thread.stop()
		exit()

	def add_new_device(self, dev):
		print dev
		self.w.entry.set_text(dev['name'])

	def __init__(self):
		self.menu_items = (
			( "/_File", \
							None,			None,				0, "<Branch>" ),
			( "/File/E_xit", \
							"<control>Q",	self._quit,			0, None ),
			( "/_Devices", \
							None,			None,				0, "<Branch>" ),
			( "/Devices/_Disable notification", \
							None,			None,				0, None ),
			( "/Devices/Disable notif for _all", \
							None,			None,				0, None ),
			( "/_Actions", \
							None,			None,				0, "<Branch>" ),
			( "/Actions/on _Disable notif", \
							None,			None,				0, None ),
			( "/Actions/_Apply all actions", \
							None,			None,				0, None ),
			( "/Actions/_Cancel actions", \
							None,			None,				0, None ),
			( "/_Help", \
							None,			None,				0, "<LastBranch>" ),
			( "/Help/About", \
							None,			None,				0, None ),
			( "/Help/About Qt", \
							None,			None,				0, None ),
			)

		self.toolbar = gtk.Toolbar()
		#self.toolbar.prepend_item(text, tooltip_text, tooltip_private_text, icon, callback, user_data)
		self.toolbar.append_item('Disable\nnotification', "Disable notification", '', \
							disable, None, user_data = None)
		self.toolbar.append_item('Disable\nnotif for all', "Disable notif for all", '', \
							disableall, None, user_data = None)
		self.toolbar.append_item('Apply\nall actions', "Apply all actions", '', \
							apply_, None, user_data = None)
		self.toolbar.append_item('Delete\naction', "Delete action", '', \
							deleteaction, None, user_data = None)
		self.toolbar.append_item('Cancel\nactions', "Cancel actions", '', \
							cancelaction, None, user_data = None)
		#self.toolbar.append_space()
		self.toolbar.prepend_space()
		self.toolbar.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
		#self.toolbar.insert_space(position)
		self.toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
		self.toolbar.set_style(gtk.TOOLBAR_ICONS)
		self.toolbar.set_border_width(1)

		self.listDev = gtk.TreeView()
		self.listDev.set_tooltip_text('Detected Devices')
		self.listDev.set_size_request(200, 150)

		self.scrollWindow = gtk.ScrolledWindow()
		self.scrollWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.w = Detail(False, 1)
		self.scrollWindow.add_with_viewport(self.w)
		self.w.show_all()

		#self.detail = gtk.VBox(False, 1)
		self.detail = gtk.Frame()
		self.detail.set_label('Modules')
		self.detail.set_tooltip_text('Module details')
		self.detail.set_border_width(1)
		self.detail.add(self.scrollWindow)
		self.scrollWindow.show()

		self.hpaned = gtk.HPaned()
		self.hpaned.add1(self.listDev)
		self.hpaned.add2(self.detail)
		self.hpaned.set_size_request(600, 300)
		self.listDev.show()
		self.detail.show()

		self.text = gtk.TreeView()
		self.text.set_tooltip_text('Actions')
		self.text.set_size_request(600, 250)

		self.vpaned = gtk.VPaned()
		self.vpaned.add1(self.hpaned)
		self.vpaned.add2(self.text)
		self.hpaned.show()
		self.text.show()

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self._quit)
		self.window.set_title("GTK ScodClient")
		self.window.set_size_request(600, 500)

		self.main_vbox = gtk.VBox(False, 1)
		self.main_vbox.set_border_width(1)
		self.window.add(self.main_vbox)
		self.main_vbox.show()

		self.menubar = self.get_main_menu(self.window)

		self.main_vbox.pack_start(self.menubar, False, True, 0)
		self.main_vbox.pack_start(self.toolbar, False, True, 0)
		self.main_vbox.pack_start(self.vpaned, False, True, 0)
		self.toolbar.show()
		self.menubar.show()
		self.vpaned.show()
		self.window.show()

		self.listen_thread = ListenThread(parent_class = self.add_new_device)

def main():
	gtk.main()
	return 0

if __name__ == "__main__":
	clnt = gtkScodClient()
	clnt.listen_thread.run()
	main()
