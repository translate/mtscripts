#!/bin/bash

pushd .
cd `dirname $0`

#if [ $1 = '-h' || $1 = '--help' ] then
#	echo "./copy_po.sh <source_dir> <target_dir>"
#fi

sdir=$1
tdir=$2

mkdir -p $tdir

for d in $(cd $sdir; ls)
do
	for t in $(ls $sdir/$d/*.po)
	do
		scp $t $tdir
	done
done

popd