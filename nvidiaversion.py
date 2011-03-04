#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, os.path

class NvidiaVersion:
	def __init__(self):
		self.nvidia_driver_version = None
		self.nvidia_board_name = None
		self.nvidia_driver_ver_list=None
		self._load_info_ver()
		self._load_info_board()

	def _load_info_ver(self):
		if not os.path.exists('/proc/driver/nvidia'):
			return
		f = open('/proc/driver/nvidia/version', 'r')
		str_i = 0
		nvrm = []
		gcc = []
		for s in f:
			if str_i == 0:
				nvrm = s.split()
			else:
				gcc = s.split()
			str_i += 1
		f.close()

		if len(nvrm) >= 8:
			self.nvidia_driver_version = nvrm[7]
			self.nvidia_driver_ver_list= nvrm[7].split('.')
	
	def _load_info_board(self):
		bn = []
		proc_dir = '/proc/driver/nvidia/cards'
		if not os.path.exists(proc_dir):
			return
		
		for d in os.listdir(proc_dir):
			f = open (os.path.join(proc_dir, d), 'r')
			for s in f:
				if ('Model' in s) and (len(s.split(':')) > 1):
					bn.append(s.split(':')[1].strip())
			f.close()

		self.nvidia_board_name = str.join('/', bn)
			

if __name__ == '__main__':
	q = NvidiaVersion()
	print "Module version: %s (%s)" % (q.nvidia_driver_version, q.nvidia_driver_ver_list)
	print 'Board name: %s' % q.nvidia_board_name


