#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from Detail import Detail
from Image import *
from ListenThread import ListenThread

class gtkScodClient:
	# Obligatory basic callback
	def print_hello(self, w, data):
		print "Hello, World!"

	def get_main_menu(self, window):
		accel_group = gtk.AccelGroup()

		# This function initializes the item factory.
		# Param 1: The type of menu - can be MenuBar, Menu,
		#		  or OptionMenu.
		# Param 2: The path of the menu.
		# Param 3: A reference to an AccelGroup. The item factory sets up
		#		  the accelerator table while generating menus.
		item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)

		# This method generates the menu items. Pass to the item factory
		#  the list of menu items
		item_factory.create_items(self.menu_items)

		# Attach the new accelerator group to the window.
		window.add_accel_group(accel_group)

		# need to keep a reference to item_factory to prevent its destruction
		self.item_factory = item_factory
		# Finally, return the actual menu bar created by the item factory.
		return item_factory.get_widget("<main>")

	def __init__(self):
		self.menu_items = (
			( "/_File", \
							None,			None,				0, "<Branch>" ),
			( "/File/E_xit", \
							"<control>Q",	gtk.main_quit,		0, None ),
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

		toolbar = gtk.Toolbar()
		#toolbar.prepend_item(text, tooltip_text, tooltip_private_text, icon, callback, user_data)
		toolbar.append_item('Disable\nnotification', "Disable notification", '', \
							disable, None, user_data = None)
		toolbar.append_item('Disable\nnotif for all', "Disable notif for all", '', \
							disableall, None, user_data = None)
		toolbar.append_item('Apply\nall actions', "Apply all actions", '', \
							apply_, None, user_data = None)
		toolbar.append_item('Delete\naction', "Delete action", '', \
							deleteaction, None, user_data = None)
		toolbar.append_item('Cancel\nactions', "Cancel actions", '', \
							cancelaction, None, user_data = None)
		#toolbar.append_space()
		toolbar.prepend_space()
		toolbar.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
		#toolbar.insert_space(position)
		toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
		toolbar.set_style(gtk.TOOLBAR_ICONS)
		toolbar.set_border_width(1)

		listDev = gtk.TextView()
		listDev.set_tooltip_text('Detected Devices')
		listDev.set_size_request(200, 150)

		scrollWindow = gtk.ScrolledWindow()
		scrollWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		scrollWindow.add_with_viewport(Detail)
		Detail.show()

		#detail = gtk.VBox(False, 1)
		detail = gtk.Frame()
		detail.set_label('Modules')
		detail.set_tooltip_text('Module details')
		detail.set_border_width(1)
		detail.add(scrollWindow)
		scrollWindow.show()

		hpaned = gtk.HPaned()
		hpaned.add1(listDev)
		hpaned.add2(detail)
		hpaned.set_size_request(600, 300)
		listDev.show()
		detail.show()

		text = gtk.TreeView()
		text.set_tooltip_text('Actions')
		text.set_size_request(600, 250)

		vpaned = gtk.VPaned()
		vpaned.add1(hpaned)
		vpaned.add2(text)
		hpaned.show()
		text.show()

		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.connect("destroy", lambda w: gtk.main_quit())
		window.set_title("GTK ScodClient")
		window.set_size_request(600, 500)

		main_vbox = gtk.VBox(False, 1)
		main_vbox.set_border_width(1)
		window.add(main_vbox)
		main_vbox.show()

		menubar = self.get_main_menu(window)

		main_vbox.pack_start(menubar, False, True, 0)
		main_vbox.pack_start(toolbar, False, True, 0)
		main_vbox.pack_start(vpaned, False, True, 0)
		toolbar.show()
		menubar.show()
		vpaned.show()
		window.show()

		self.listen_thread = ListenThread(self)

def main():
	gtk.main()
	return 0

if __name__ == "__main__":
	clnt = gtkScodClient()
	clnt.listen_thread.start()
	main()
