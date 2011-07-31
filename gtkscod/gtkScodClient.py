#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
from Image import *
from Processing import WindowProcessing

class gtkScodClient:

	def get_main_menu(self, window):
		accel_group = gtk.AccelGroup()
		item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
		item_factory.create_items(self.menu_items)
		window.add_accel_group(accel_group)
		self.item_factory = item_factory
		return item_factory.get_widget("<main>")

	def _quit(self, *args):
		#print args
		self.proc.lt.stop()
		exit()

	def __init__(self):

		self.proc = WindowProcessing(self)

		self.menu_items = (
			( "/_File", \
							None,			None,			0,	"<Branch>" ),
			( "/File/E_xit", \
							"<control>Q",	self._quit,		1,	None ),
			( "/_Devices", \
							None,			None,			2,	"<Branch>" ),
			( "/Devices/_Disable notification", \
							None,			self.proc._handle_disable_device, \
															3,	None ),
			( "/Devices/Disable notif for _all", \
							None,			self.proc._handle_disable_all, \
															4,	None ),
			( "/_Actions", \
							None,			None,			5,	"<Branch>" ),
			( "/Actions/on _Disable notif", \
							None,			None,			6,	None ),
			( "/Actions/_Apply all actions", \
							None,			self.proc._handle_apply_actions, \
															7,	None ),
			( "/Actions/_Cancel actions", \
							None,			self.proc._handle_clean_actions, \
															8,	None ),
			( "/_Help", \
							None,			None,			9,	"<LastBranch>" ),
			( "/Help/About", \
							None,			None,			10,	None ),
			( "/Help/About Qt", \
							None,			None,			11,	None ),
			)

		self.toolbar = gtk.Toolbar()
		#self.toolbar.prepend_item(text, tooltip_text, tooltip_private_text, icon, callback, user_data)
		self.toolbar.append_item('Disable\nnotification', "Disable notification", '', \
							disable, self.proc._handle_disable_device, user_data = 'curr_Notif')
		self.toolbar.append_item('Disable\nnotif for all', "Disable notif for all", '', \
							disableall, self.proc._handle_disable_all, user_data = 'all_Notif')
		self.toolbar.append_item('Apply\nall actions', "Apply all actions", '', \
							apply_, self.proc._handle_apply_actions, user_data = 'all_apply')
		self.toolbar.append_item('Delete\naction', "Delete action", '', \
							deleteaction, self.proc._handle_remove_current_action, user_data = 'curr_act_del')
		self.toolbar.append_item('Cancel\nactions', "Cancel actions", '', \
							cancelaction, self.proc._handle_clean_actions, user_data = 'actions_clear')
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

		self.tvcolumn = gtk.TreeViewColumn('Detected Devices')
		self.listDev.append_column(self.tvcolumn)
		self.cellpb = gtk.CellRendererPixbuf()
		self.cell = gtk.CellRendererText()
		self.tvcolumn.pack_start(self.cellpb, False)
		self.tvcolumn.pack_start(self.cell, True)
		self.tvcolumn.set_attributes(self.cellpb, stock_id=1)
		self.tvcolumn.set_attributes(self.cell, text=0)

		self.scrollWindow = gtk.ScrolledWindow()
		self.scrollWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.Detail = self.proc.Detail
		self.scrollWindow.add_with_viewport(self.Detail)

		self.detail = gtk.Frame()
		self.detail.set_label('Modules')
		self.detail.set_tooltip_text('Module details')
		self.detail.set_border_width(1)
		self.detail.add(self.scrollWindow)

		self.hpaned = gtk.HPaned()
		self.hpaned.add1(self.listDev)
		self.hpaned.add2(self.detail)
		self.hpaned.set_size_request(600, 300)

		self.listAct = gtk.TreeView()
		self.listAct.set_tooltip_text('Actions')
		self.listAct.set_size_request(600, 250)

		self.vpaned = gtk.VPaned()
		self.vpaned.add1(self.hpaned)
		self.vpaned.add2(self.listAct)

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self._quit)
		self.window.set_title("GTK ScodClient")
		self.window.set_size_request(600, 500)

		self.main_vbox = gtk.VBox(False, 1)
		self.main_vbox.set_border_width(1)
		self.window.add(self.main_vbox)

		self.menubar = self.get_main_menu(self.window)

		self.main_vbox.pack_start(self.menubar, False, True, 0)
		self.main_vbox.pack_start(self.toolbar, False, True, 0)
		self.main_vbox.pack_start(self.vpaned, False, True, 0)

		self.proc._init_models()
		self.window.hide_all()

if __name__ == "__main__" :
	try :
		clnt = gtkScodClient()
		clnt.proc.start_listen()
		gtk.main()
	except KeyboardInterrupt , err :
		print "close manually"
		exit()
