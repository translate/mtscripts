#!/bin/bash

pushd .
cd `dirname $0`

sdir=4.reviewed
tdir=5.po-files

mkdir -p $tdir
for d in $(cd $sdir; ls)
do
	echo $d
	for t in $(ls $sdir/$d/*.po)
	do
		cp $t $tdir
		#cp $t $tdir
		#r=$t
	done
done

popd