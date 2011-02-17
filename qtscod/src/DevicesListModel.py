#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4.QtCore import Qt, QAbstractListModel, QModelIndex
from PyQt4.QtGui import QIcon
from src.Device import Device

class DevicesListModel(QAbstractListModel):
	def __init__(self, parent = None):
		QAbstractListModel.__init__(self, parent)
		self.data_list = []
		self.load_img()
		self.update_model()

	def load_img(self):
		self.wifi_icon = QIcon("img/wifi.svg")
		self.hard_icon = QIcon("img/hardware.svg")
		
	# Common methods
	def columnCount( self, parent = QModelIndex() ):
		return 1

	def rowCount( self, parent = QModelIndex() ):
		return len(self.data_list)

	def headerData( self, section, orientation, role = Qt.DisplayRole ):
		if ( orientation == Qt.Vertical): #Qt.Horizontal ):
			if ( role == Qt.DisplayRole ):
				if section == 0:
					return self.tr("Device name")
				#elif section == 1:
				#	return self.tr("Device type")

		return QtCore.QVariant()

	def data ( self, idx, role = Qt.DisplayRole ):
		d = self.data_list[idx.row()]
		if role == Qt.DisplayRole:
			if idx.column() == 1:
				return d.device_type()
			elif idx.column() == 0:
				return QtCore.QString(d.device_name())
		elif role == Qt.DecorationRole:
			if d.device_type() == 'net':
				return self.wifi_icon
			else:
				return self.hard_icon

		return QtCore.QVariant()

	# Manipulate with data
	def add_new_device(self, dev):
		d = Device(dev)
		self.data_list.append(d)
		print "Device added: %s (%s)" % (d.device_name(), d.device_type())
		self.dataChanged.emit(self.index(len(self.data_list)-1, 0),self.index(len(self.data_list)-1, 1))
		#self.update_model()

	def update_model(self):
		self.beginResetModel()
		self.endResetModel()

	def device_by_index(self, idx):
		if len(self.data_list) < idx.row()-1:
			return None

		return self.data_list[idx.row()]
