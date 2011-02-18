#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4.QtCore import Qt, QAbstractListModel, QModelIndex, QVariant, QString
from PyQt4.QtGui import QIcon

''' Some action dict example
	act_dict['name'] = module_name 			# 'nvidia' as example
	act_dict['type'] = 0 or 1				# 0 - to install, 1 - to remove
	act_dict['pkgs'] = packages_to_action	# ['akmod-simple-2.3', 'kmod-simple-2.3*']
'''
class ActionsModel(QAbstractListModel):
	def __init__(self, parent = None):
		QAbstractListModel.__init__(self, parent)
		self._load_imgs()
		self.actions = [] # main data container

	def _load_imgs(self):
		self.gears_icon = QIcon("img/gears.svg")	

	def _view_name(self, act):
		act_type = self.tr('Installing')
		if act['type'] == 1:
			act_type = self.tr('Removing')
		act_module	= act['name']
		act_sp		= self.tr('packages')
		act_p		= str(', ').join(act['pkgs'])

		res = QString('%1 %2 (%3: %4)').arg(act_type).arg(act_module).arg(act_sp).arg(act_p)
		return res

	def add_new_action(self, name, pkgs = [], atype=0):
		ad = {}
		ad['name']	= name
		ad['type']	= atype
		ad['pkgs']	= pkgs
		self.actions.append(ad)
		self.dataChanged.emit(self.index(len(self.actions)-1, 0),self.index(len(self.actions)-1, 0))

	# commons
	def columnCount( self, parent = QModelIndex() ):
		return 1
	def rowCount( self, parent = QModelIndex() ):
		return len(self.actions)
	def headerData( self, section, orientation, role = Qt.DisplayRole ):
		if section == 0 and role == Qt.DisplayRole:
			return tr('Action description')
		return QVariant()
	def data( self, idx, role = Qt.DisplayRole ):
		act_dict = self.actions[idx.row()]
		if role == Qt.DisplayRole:
			if idx.column() == 0:
				return self._view_name(act_dict)
		elif role == Qt.DecorationRole:
			return self.gears_icon

		return QVariant()
