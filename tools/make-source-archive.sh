#!/bin/sh

APP_NAME=scod
APP_VERSION=0.1.git`date +%Y%m%d`
APP_ANAME=$APP_NAME-$APP_VERSION

cd ../..
cp -f -r ./$APP_NAME ./$APP_ANAME
rm -rf ./$APP_ANAME/.git

find ./$APP_ANAME -name *.pyc -exec rm -rf {} \;
find ./$APP_ANAME -name *~ -exec rm -rf {} \;
rm -rf ./$APP_ANAME/qtscod/ui/*.py*
touch ./$APP_ANAME/qtscod/ui/__init__.py

tar cfj $APP_ANAME.tar.bz2 ./$APP_ANAME
rm -rf ./$APP_ANAME
