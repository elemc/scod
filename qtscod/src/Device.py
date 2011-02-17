#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Device:
	def __init__(self, dev = None):
		self._name				= ""
		self._type				= ""
		self._id				= ""
		self._modules			= {}
		self._current_driver	= ""

		if dev is not None:
			self.set_dev(dev)


	def _extract_data(self, data, name):
		if name in data.keys():
			return data[name]
		return ""

	def set_dev(self, dev):
		self._name				= self._extract_data(dev, 'name')
		self._type				= self._extract_data(dev, 'type')
		self._id				= self._extract_data(dev, 'id')
		self._modules			= self._extract_data(dev, 'modules')
		self._current_driver	= self._extract_data(dev, 'current_driver')

	def current_driver(self):
		return self._current_driver
	def device_name(self):
		return self._name
	def device_type(self):
		return self._type
	def device_id(self):
		return self._id
	def device_modules(self):
		return self._modules.keys()
	def device_package_by_module(self, module):
		if module in self._modules.keys():
			return self._modules[module]
		return []
