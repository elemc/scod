#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

class ActionsModel(gtk.ListStore):
	def __init__(self, parent = None):
		gtk.ListStore.__init__(self, str)

		self.Parent = parent
		self.set_column_types(str, str)
		self.actions = [] # main data container

	def add_new_action(self, devid, name, pkgs = [], atype=0):
		ad = {}
		ad['devid']	  = devid
		ad['name']	  = name
		ad['type']	  = atype
		ad['pkgs']	  = pkgs
		self.actions.append(ad)
		self.append([self._view_name(ad), gtk.STOCK_ADD])

	def _view_name(self, act):
		act_type = 'Installing'
		if act['type'] == 1:
			act_type = 'Removing'
		act_module = act['name']
		act_sp = 'packages'
		act_p = str(', ').join(act['pkgs'])

		res = '%s %s (%s: %s)' % (act_type, act_module, act_sp, act_p)
		return res

	# commons
	def removeCurrAct(self, idx):
		value = self.get_value(idx, 0)
		self.remove(idx)
		for act in self.actions :
			if self._view_name(act) == value :
				self.actions.remove(act)
				break

	def clearRows(self):
		self.clear()
		self.actions = []

	def remove_actions_by_devid(self, sel_dev_id, module_name):
		act_to_remove = {}
		for act in self.actions:
			if act['devid'] == sel_dev_id: # and act['name'] != module_name:
				row = self.actions.index(act)
				act_to_remove[row] = act
				self.remove(self.get_iter((0, row)))
		for idx in act_to_remove.keys():
			self.actions.remove(act_to_remove[idx])

	def get_packages(self, _install_akmods = False):
		pkgs_to_install = []
		pkgs_to_remove = []
		for act in self.actions:
			for p in act['pkgs']:
				if act['type'] == 0:
					pkgs_to_install.append(p)
					if _install_akmods:
						pkgs_to_install.append('a%s' % p)
				elif act['type'] == 1:
					pkgs_to_remove.append('a%s' % p)
					pkgs_to_remove.append(p)
		
		return (pkgs_to_install,pkgs_to_remove)

	def pkgs_to_install_exist(self):
		ret_res = False
		for act in self.actions:
			if act['type'] == 0:
				ret_res = True
		return ret_res
