#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class KernelVariant:
	def __init__(self, ver = None):
		self.kernel_version = None

		if ver is None:
			self.kernel_info = self._load_version()
		else:
			self.kernel_info = self._parse_version(ver.split())

	def _param(self, resource, index):
		if len(resource) >= index+1:
			return resource[index];
		return None

	def _version_info(self, ver):
		kinfo = {}
		v = ver.split('.')
		kinfo['a']			= self._param(v, 0)
		kinfo['b']			= self._param(v, 1)
		kinfo['c']			= self._param(v, 2)
		kinfo['release']	= self._param(v, 3)
		kinfo['distr']		= self._param(v, 4)
		kinfo['arch']		= self._param(v, 5)
		kinfo['kvariant']	= self._param(v, 6)
		return kinfo

	def _parse_version(self, res):
		k = {}
		k['system'] 	= self._param(res, 0)
		k['version']	= self._param(res, 2)
		self.kernel_version = self._version_info(k['version'])
		k['bhost']		= self._param(res, 3)

		if len(res) >= 14:
			k['bsign']	= str.join(' ', res[4:13])
		
		if len(res) >= 19:
			k['bdate']	= str.join(' ', res[15:20])
		return k


	def _load_version(self):
		res = []
		proc_version = open('/proc/version', 'r')
		for s in proc_version:
			if len(s) != 0:
				res = s.split()
		proc_version.close()
		return self._parse_version(res)
		

if __name__ == '__main__':
	if len(sys.argv) == 1:
		q = KernelVariant()
	else:
		q = KernelVariant(sys.argv[1])

	for k in q.kernel_version.keys():
		print "%s = %s" % (k, q.kernel_version[k])
