#!/bin/sh

QTSCOD_DATAROOT_DIR=/usr/share/qtscod
PYTHON=/usr/bin/python

if [ -x $PYTHON ]; then
    $PYTHON $QTSCOD_DATAROOT_DIR/qtscod.py $*
else
    echo "Python not found."
fi