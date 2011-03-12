#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4.QtCore import Qt, QAbstractListModel, QModelIndex, QVariant, QString, pyqtSignal
from PyQt4.QtGui import QIcon

''' Some action dict example
    act_dict['devid']= device_id            # sys_path for device
    act_dict['name'] = module_name          # 'nvidia' as example
    act_dict['type'] = 0 or 1                   # 0 - to install, 1 - to remove
    act_dict['pkgs'] = packages_to_action   # ['akmod-simple-2.3', 'kmod-simple-2.3*']
'''
class ActionsModel(QAbstractListModel):
    actionDeleted = pyqtSignal(str)

    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self._load_imgs()
        self.actions = [] # main data container

    def _load_imgs(self):
        self.gears_icon = QIcon("../img/gears.svg")     

    def _view_name(self, act):
        act_type = self.tr('Installing')
        if act['type'] == 1:
            act_type = self.tr('Removing')
        act_module  = act['name']
        act_sp      = self.tr('packages')
        act_p       = str(', ').join(act['pkgs'])

        res = QString('%1 %2 (%3: %4)').arg(act_type).arg(act_module).arg(act_sp).arg(act_p)
        return res

    def add_new_action(self, devid, name, pkgs = [], atype=0):
        ad = {}
        ad['devid']     = devid
        ad['name']      = name
        ad['type']      = atype
        ad['pkgs']      = pkgs
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
    def removeRows(self, row, count, parent = QModelIndex()):
        last = row + count - 1
        self.beginRemoveRows(parent, row, last)
        remove_items = []
        remove_range = range(row, last)
        if count == 1:
            remove_range = [row]
        for a in self.actions:
            if self.actions.index(a) in remove_range:
                remove_items.append(a)
        for ra in remove_items:
            self.actions.remove(ra)
            self.actionDeleted.emit(ra['devid'])
        self.endRemoveRows()

    def clearRows(self):
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount())
        for act in self.actions:
            self.actionDeleted.emit(act['devid'])
        self.actions = []
        self.endRemoveRows()

    def remove_actions_by_devid(self, sel_dev_id, module_name):
        act_to_remove = {}
        for act in self.actions:
            if act['devid'] == sel_dev_id: # and act['name'] != module_name:
                row = self.actions.index(act)
                act_to_remove[row] = act
        for idx in act_to_remove.keys():
            self.actions.remove(act_to_remove[idx])
            self.dataChanged.emit(self.index(idx, 0), self.index(idx, 0))

    def get_packages(self, _install_akmods = False):
        pkgs_to_install = []
        pkgs_to_remove = []
        for act in self.actions:
            for p in act['pkgs']:
                if act['type'] == 0:
                    pkgs_to_install.append(p)
                    if _install_akmods:
                        pkgs_to_install.append('a%s' % p)
                elif act['type'] == 1:
                    pkgs_to_remove.append('a%s' % p)
                    pkgs_to_remove.append(p)
        
        return (pkgs_to_install,pkgs_to_remove)

    def pkgs_to_install_exist(self):
        ret_res = False
        for act in self.actions:
            if act['type'] == 0:
                ret_res = True
        return ret_res
