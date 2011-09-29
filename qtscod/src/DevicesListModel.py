#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4.QtCore import Qt, QAbstractListModel, QModelIndex, QString
from PyQt4.QtGui import QIcon, QBrush
from src.Device import Device

import qtscod_rc

class DevicesListModel(QAbstractListModel):
    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self.data_list = []
        self.load_img()
        self.update_model()

    def load_img(self):
        self.wifi_icon = QIcon(":/img/wifi")
        self.hard_icon = QIcon(":/img/hardware")
        
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
                #       return self.tr("Device type")

        return QtCore.QVariant()

    def data ( self, idx, role = Qt.DisplayRole ):
        d = self.data_list[idx.row()]
        if role == Qt.DisplayRole:
            if idx.column() == 1:
                return d.device_type()
            elif idx.column() == 0:
                dname = QString(d.device_name())
                if d.is_hide():
                    dname = QString("%1 (%2)").arg(dname).arg(self.tr("disable notification"))
                return dname
        elif role == Qt.DecorationRole:
            if d.device_type() == 'net':
                return self.wifi_icon
            else:
                return self.hard_icon
        elif role == Qt.TextColorRole:
            if len(d.selected_driver()) != 0:
                blue_brush = QBrush()
                blue_brush.setColor(Qt.darkBlue)
                return blue_brush

        return QtCore.QVariant()

    # Manipulate with data
    def add_new_device(self, dev):
        d = Device(dev)
        self.data_list.append(d)
        print "Device added: %s (%s)" % (d.device_name(), d.device_type())
        self.dataChanged.emit(self.index(len(self.data_list)-1, 0),self.index(len(self.data_list)-1, 1))

    def update_model(self):
        self.beginResetModel()
        self.endResetModel()

    def device_by_index(self, idx):
        if len(self.data_list) < idx.row()-1:
            return None

        return self.data_list[idx.row()]
    
    def index_is_hide(self, idx):
        if len(self.data_list) < idx.row()-1:
            return False

        return self.data_list[idx.row()].is_hide()
    
    def index_hide(self, idx, val = True):
        if len(self.data_list) < idx.row()-1:
            return
        d = self.data_list[idx.row()]
        d.set_hide(val)
        self.dataChanged.emit(idx, idx)
        return d.device_id()
    
    def disable_all_devices(self):
        ret_devs = []
        for d in self.data_list:
            d.set_hide(True)
            ret_devs.append(d.device_id())
        self.dataChanged.emit(self.index(0,0), self.index(self.rowCount()-1, 0))
        return ret_devs

    def reset_changes(self, dev_id):
        for d in self.data_list:
            if d.device_id() == dev_id:
                d.set_selected_driver('')
                row = self.data_list.index(d)
                self.dataChanged.emit(self.index(row,0), self.index(row,0))
