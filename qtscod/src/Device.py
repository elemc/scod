#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Device:
	def __init__(self, dev = None):
		self._name			= ""
		self._type			= ""
		self._id		        = ""
		self._modules		        = {}
		self._current_driver            = ""
		self._hide_this                 = False
		self._selected_driver	        = ""

		if dev is not None:
			self.set_dev(dev)


	def _extract_data(self, data, name):
		if name in data.keys():
			return data[name]
		return ""

	def set_dev(self, dev):
		self._name		= self._extract_data(dev, 'name')
		self._type		= self._extract_data(dev, 'type')
		self._id		= self._extract_data(dev, 'id')
		self._modules		= self._extract_data(dev, 'modules')
		self._current_driver	= self._extract_data(dev, 'current_driver')

	def set_hide(self, val = True):
		self._hide_this = val
	def is_hide(self):
		return self._hide_this

	def selected_driver(self):
		return self._selected_driver
	def set_selected_driver(self, newdrv):
		self._selected_driver = newdrv
	def current_driver(self):
		return self._current_driver
	def device_name(self):
		return self._name
	def device_type(self):
		return self._type
	def device_id(self):
		return self._id
	def device_modules(self, exclude_module_name = None):
		if exclude_module_name is None:
			return self._modules.keys()
		else:
			temp_m = []
			for m in self._modules:
				if m == exclude_module_name:
					continue
				temp_m.append(m)
			return temp_m
	def device_package_by_module(self, module):
		if module in self._modules.keys():
			return self._modules[module]
		return []

	def packages_to_install(self, module):
		pkgs = self.device_package_by_module(module)
		return pkgs

	def packages_to_remove(self, module):
		pkgs = []
		for m in self._modules:
			if m == module:
				continue

			pkgs += self.device_package_by_module(m)

		return pkgs
