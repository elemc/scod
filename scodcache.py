#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path, os

class SCODCache:
    def __init__(self):
        self._cache_dir    = '/var/cache/scod'
        self._ddn_filename = 'disabled_devices.list'
        self._ddn_full     = os.path.join(self._cache_dir, self._ddn_filename)
        self.check_cache_dir()

    def _warn_msg(self, msg):
        pass
        #print "Warning: %s" % msg

    def _err_msg(self, msg):
        print "Error: %s" % msg

    def check_cache_dir(self):
	if not os.path.exists(self._cache_dir):
            self._warn_msg('Directory %s not exists. Try to create it...')
            try:
                os.makedirs(self._cache_dir, 0755)
            except:
                self._err_msg("Directory %s doesn't create. Maybe access denied?" % self._cache_dir)
		return False
        return True

    def read_ddn(self):
        ret_res = []
        if not os.path.exists(self._ddn_full):
            self._warn_msg("File %s doesn't exist" % self._ddn_full)
            return ret_res
        
        try:
            ddn = open(self._ddn_full, 'r')
        except:
            self._err_msg("File %s doesn't open for read" % self._ddn_full)
            return ret_res

        for s in ddn:
            ret_res.append(s.strip())
        ddn.close()
        return ret_res
        
    def add_to_ddn(self, src, open_attr = 'a'):
        if not self.check_cache_dir():
            return False
        
	try:
            ddn_file = open(self._ddn_full, open_attr)
	except:
            self._err_msg("Open file to append failed [%s]." % ddn_filename)
            return False
	
        if type(src) is list:
            for s in src:
                ddn_file.write('%s\n' % s)
        else:
            ddn_file.write('%s\n' % src)
	ddn_file.close()
	return True
        
    def del_from_ddn(self, src):
        cont = self.read_ddn()
        if type(src) is list:
            for s in src:
                while s in cont:
                    cont.remove(s)
        else:
            while src in cont:
                cont.remove(src)

        if len(cont) == 0:
            try:
                os.remove(self._ddn_full)
            except:
                self._warn_msg('File %s not exists. Nothing to remove.' % self._ddn_full)
                return True
        else:
            self.add_to_ddn(cont, 'w')

        return True
        
