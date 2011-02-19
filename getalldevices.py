# -*- coding: utf-8 -*-

from pyudev import Context
import sys

def uni(s):
	us = s.decode('utf-8', 'ignore')
	return us

#sys.setdefaultencoding("UTF-8")
context = Context()
for dev in context.list_devices():
	print "Device: %s" % dev.sys_path
	print "  Name: %s" % dev.sys_name
	print "  Driver: %s" % dev.driver
	if dev.parent is not None:
		print "  Parent: %s" % dev.parent.sys_path
	print "  Keys:"
	for m in dev.keys():
		print "    %s = %s" % (m, dev[m])
	print "  Attr:"
	for a in dev.attributes.keys():
		print "    %s = %s" % (uni(a), uni(dev.attributes[a]))

