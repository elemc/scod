#!/bin/sh

SCODD_DATAROOT_DIR=/usr/share/scodd
PYTHON=/usr/bin/python

if [ -x $PYTHON ]; then
    $PYTHON $SCODD_DATAROOT_DIR/scodd.py $*
else
    echo "Python not found."
fi