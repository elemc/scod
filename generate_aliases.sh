#!/bin/sh

MODINFO=/sbin/modinfo
RPM=/bin/rpm

for m in $*; do
	license=`$MODINFO $m | grep license | awk '{print $2}'`
	aliases=`$MODINFO $m | grep alias | awk '{print $2}'`
	filename=`$MODINFO $m | grep filename | awk '{print $2}'`
	package=`$RPM -qf $filename`
	modulename=$m

	
	cat <<EOF
[$modulename]
license=$license
packages=$package
EOF
	al_sect=""
	for al in $aliases; do
		al_sect="${al_sect} ${al}"
		#echo "alias=${al}"
	done
	echo "aliases=${al_sect}"
	echo ''
done

