#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyQt4.QtCore
from PyQt4.QtCore import QAbstractListModel, QModelIndex

class DevicesListModel(QAbstractListModel):
	def __init__(self, parent = None):
		QAbstractListModel.__init__(self, parent)
		self.data_list = []

	# Common methods
	def columnCount( self, parent = QModelIndex() ):
		return 2

	def rowCount( self, parent = QModelIndex() ):
		return len(self.data_list)

	def headerData( self, section, orientation, role = QtCore.DisplayRole ):
		if ( orientation == QtCore.Horizontal ):
			if ( role == QtCore.DisplayRole ):
				if section == 0:
					return self.tr("Device name")
				elif section == 1:
					return self.tr("Device type")

		return QtCore.QVariant()

	def data ( self, idx, role = QtCore.DisplayRole ):
		d = self.data_list[idx.row()]
		if role == QtCore.DisplayRole:
			if idx.column() == 1:
				return d.device_type()
			elif idx.column() == 0:
				return d.device_name()

	# Manipulate with data
	def add_new_device(self, dev):
		self.data_list.append(dev)
		self.dataChanged.emit(self.index(len(self.data_list)-1, 0),self.index(len(self.data_list)-1, 1))



	#def insertRows( self, row, count, parent = QModelIndex() ):
	#def removeRows( self, row, count, parent = QModelIndex() ):
