#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
from Device import Device

class DevicesListModel(gtk.ListStore):
	def __init__(self, parent = None):
		gtk.ListStore.__init__(self, str)

		self.Parent = parent
		self.set_column_types(str, str)
		self.data_list = []

	def unicalDev(self, dev):
		unicality = True
		d = Device(dev)
		for device in self.data_list :
			if d.device_name() == device.device_name() and \
			   d.device_type() == device.device_type() :
				unicality = False
				break
		return unicality

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

	def enable_all_devices(self):
		ret_devs = []
		for d in self.data_list:
			d.set_hide(False)
			ret_devs.append(d.device_id())
		curr_iter = self.get_iter_first()
		while curr_iter is not None :
			if curr_iter is None : return None, None
			value_ = self.get_value(curr_iter, 0)
			if value_.endswith("\t(disable notification)") :
				value = value_[:-23]
				self.set_value(curr_iter, 0, value)
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
		dev_id = self.data_list[self.get_path(cur_idx)[0]].device_id()
		print self.get_path(cur_idx)[0], 'get_path[0] == row', dev_id
		return dev_id, res
