#!/bin/bash

#download files from server
pushd .

server=$1
servpath=$2
servdir=$3
locpath=$4
locdir=$5
datadir=$6

ssh $server "cd $servpath; sh copy_po.sh $servdir $locdir"
scp $server:$servpath/$locdir/* $locpath/$datadir/$locdir

popd