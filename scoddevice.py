# Python class for SCOD Device

import ConfigParser
from pyudev import Context
from nvidiaversion import NvidiaVersion

class SCODDevice:
	def __init__(self, dev):
		self.conffile = '/home/alex/workspace/scod/devices.conf'
		self.our_devices = {}
		self._init_configs()

		self.dev_type		= ""
		self.dev_id			= ""
		self.dev_modules	= {}
		self.dev_name		= ""
		self.dev_driver		= ""

		if dev is not None:
			self._check_device(dev)

	def __del__(self):
		self.our_devices.clear()

	def isOurDevice(self):
		if len(self.dev_modules)*len(self.dev_id) == 0:
			return False
		return True

	def _mod_search(self, pattern, mod):
		plist = pattern.split('*')
		next_start = 0
		for l in plist:
			f = mod.find(l, next_start)
			if f == -1:
				return False
			next_start = f + len(l) - 1
		return True

	def _check_mod(self, mod):
		for module in self.our_devices.keys():
			m = self.our_devices[module]
			aliases = m['aliases']
			for al in aliases:
				if self._mod_search(al, mod):
					self.dev_modules[module] = m['packages']

	def _check_device(self, dev):
		mod_name_key = 'MODALIAS'
		mod_name_attr= 'modalias'
		mod = ""
		if mod_name_key in dev.keys():
			mod = dev[mod_name_key]
		elif mod_name_attr in dev.attributes.keys():
			mod = dev.attributes[mod_name_key]
		else:
			return

		self.dev_driver = dev.driver
		self._check_mod(mod)
		self._device_name(dev)
		self.our_devices.clear()
		
	def _device_name(self, dev):
		self.dev_id = str(dev.sys_path)
		# check is a wifi?
		C = Context()
		dev_childs = C.list_devices(subsystem='net')
		for c in dev_childs:
			if c.parent == dev:
				self.dev_type = 'net'
				if ( 'ID_VENDOR_FROM_DATABASE' in c.keys() ) and ( 'ID_MODEL_FROM_DATABASE' in c.keys()  ):
					self.dev_name = "%s %s" % (str(c['ID_VENDOR_FROM_DATABASE']), str(c['ID_MODEL_FROM_DATABASE']))
					break
				else:
					self.dev_name = 'Unknown wifi adapter'
					break
			

		if len(self.dev_name) != 0:
			return

		# check is a video?
		if 'PCI_ID' in dev.keys():
			pci_id = dev['PCI_ID']
			vendor_id = pci_id[:4]

			if vendor_id == '10DE':
				self.dev_name = 'NVIDIA video adapter'
				nv = NvidiaVersion()
				if nv.nvidia_board_name is not None:
					self.dev_name = 'NVIDIA %s' % nv.nvidia_board_name
				if nv.nvidia_driver_ver_list is not None:
					major_module_ver = nv.nvidia_driver_ver_list[0]
					if major_module_ver == '173':
						self.dev_driver = 'nvidia-173xx'
					elif major_module_ver == '96':
						self.dev_driver = 'nvidia-96xx'
			elif vendor_id == '1002':
				self.dev_name = 'ATI video adapter'

			self.dev_type = 'video'
		else:
			self.dev_name = 'Unknown videoadapter'
			self.dev_type = 'video'

	def _init_configs(self):
		config = ConfigParser.RawConfigParser()
		config.read(self.conffile)
		for sect in config.sections():
			aliases = []
			license = ""
			packages = []
			for key, value in config.items(sect):
				if key == 'license':
					license = value
				elif key == 'packages':
					packages = value.split()
				elif key == 'aliases':
					list_v = value.split()
					aliases = list_v
			
			s = {}
			s['license'] = license
			s['packages'] = packages
			s['aliases'] = aliases
			self.our_devices[sect] = s
