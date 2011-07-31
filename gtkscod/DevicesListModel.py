#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
from Device import Device

class DevicesListModel(gtk.ListStore):
	def __init__(self, parent = None):
		gtk.ListStore.__init__(self, str)

		self.set_column_types(str, str)
		self.data_list = []

	def add_new_device(self, dev):
		d = Device(dev)
		self.data_list.append(d)
		print "Device added: %s (%s)" % (d.device_name(), d.device_type())
		item = self.append([dev['name'], gtk.STOCK_PREFERENCES])
		#item = self.append([dev['name'], gtk.STOCK_ADD])

	def device_by_index(self, cur_idx):
		if cur_idx == -1 :
			return None
		return self.data_list[cur_idx]

	def disable_all_devices(self):
		ret_devs = []
		for d in self.data_list:
			d.set_hide(True)
			ret_devs.append(d.device_id())
		curr_iter = self.get_iter_first()
		while curr_iter is not None :
			self.disable_one_device(curr_iter, True)
			curr_iter = self.iter_next(curr_iter)
		return ret_devs

	def disable_one_device(self, cur_idx = None, disableAll = False):
		if cur_idx is None : return None, None
		value_ = self.get_value(cur_idx, 0)
		res = None
		if value_.endswith("\t(disable notification)") :
			value = value_[:-23]
			res = True
			if disableAll : return
		else :
			value = value_ + "\t(disable notification)"
			res = False
		self.set_value(cur_idx, 0, value)
		row = self.curr_row(cur_idx)
		dev_id = self.data_list[row].device_id()
		return dev_id, res

	def curr_row(self, curr_iter):
		first_iter = self.get_iter_first()
		row = -1
		while first_iter is not None :
			row += 1
			if first_iter == curr_iter : break
			first_iter = self.iter_next(first_iter)
		return row
