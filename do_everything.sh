#!/bin/bash

#this assumes no ssh connection is needed

pushd .

datadir='data'
podir='PO-files'
alltransdir='po-translations'
allaligndir='po-alignments'
segtransdir='seg-translations'
mkdir $datadir
cd $datadir
mkdir $podir
mkdir $alltransdir
mkdir $segtransdir
mkdir $allaligndir
cd ..

sourcepath='/var/samba/public/mt-work'
targetpath='/home/laurette/Translate_org_za/trunk/mtscripts'
transdir='translations'
aligndir='alignment'

echo $alltransdir
cp $sourcepath/$transdir/$alltransdir/* $targetpath/$datadir/$alltransdir
cp $sourcepath/$aligndir/$allaligndir/* $targetpath/$datadir/$allaligndir

#segment_po.py to segment translations

python segment_po.py $datadir/$alltransdir $datadir/$segtransdir

#pocounts for alignment and translations

#pocount 

#mkdir moses
#copy all .po files into moses/

#units_to_moses.py to get moses files
#(count moses lines or something?)

popd