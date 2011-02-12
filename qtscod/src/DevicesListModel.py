#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4.QtCore import Qt, QAbstractListModel, QModelIndex
from src.Device import Device

class DevicesListModel(QAbstractListModel):
	def __init__(self, parent = None):
		QAbstractListModel.__init__(self, parent)
		self.data_list = []
		self.update_model()

	# Common methods
	def columnCount( self, parent = QModelIndex() ):
		return 2

	def rowCount( self, parent = QModelIndex() ):
		return len(self.data_list)

	def headerData( self, section, orientation, role = Qt.DisplayRole ):
		if ( orientation == Qt.Vertical): #Qt.Horizontal ):
			if ( role == Qt.DisplayRole ):
				if section == 0:
					return self.tr("Device name")
				elif section == 1:
					return self.tr("Device type")

		return QtCore.QVariant()

	def data ( self, idx, role = Qt.DisplayRole ):
		d = self.data_list[idx.row()]
		if role == Qt.DisplayRole:
			#print "has index in row=%s and column=%s" % (idx.row(), idx.column())
			if idx.column() == 1:
				return d.device_type()
			elif idx.column() == 0:
				return QtCore.QString(d.device_name())

		return QtCore.QVariant()

	# Manipulate with data
	def add_new_device(self, dev):
		d = Device(dev)
		self.data_list.append(d)
		print "Device added: %s" % d.device_name()
		self.dataChanged.emit(self.index(len(self.data_list)-1, 0),self.index(len(self.data_list)-1, 1))

	def update_model(self):
		self.beginResetModel()
		self.endResetModel()

	#def insertRows( self, row, count, parent = QModelIndex() ):
	#def removeRows( self, row, count, parent = QModelIndex() ):
