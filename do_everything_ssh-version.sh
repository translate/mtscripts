#!/bin/bash

#need to find a way (ssh-keygen?) to prevent the password typing annoyance

pushd .

datadir='data'
mosesdir='moses'
#podir='po-files'
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

indpath='/var/samba/public/mt-work'
locpath='/home/laurette/Translate_org_za/trunk/mtscripts'
transdir='translations'
aligndir='alignment'

echo $alltransdir
ssh indlovu.local "cd $indpath/$transdir; sh copy_po.sh 4.reviewed $alltransdir"
scp indlovu.local:$indpath/$transdir/$alltransdir/* $locpath/$datadir/$alltransdir
ssh indlovu.local "cd $indpath/$aligndir; sh copy_po.sh 4.reviewed $allaligndir"
scp indlovu.local:$indpath/$aligndir/$allaligndir/* '/home/laurette/Translate_org_za/trunk/mtscripts/'$datadir/$allaligndir

#segment_po.py to segment translations

python segment_po.py $datadir/$alltransdir $datadir/$segtransdir

#pocounts for alignment and translations

pocount $datadir/$segtransdir/* | tail -n 9 > pocount_translations
pocount $datadir/$allaligndir/* | tail -n 9 > pocount_alignment

mkdir $mosesdir
#copy all .po files into moses/
cp $datadir/$segtransdir/* $mosesdir
cp $datadir/$allaligndir/* $mosesdir

#units_to_moses.py to get moses files
#(count moses lines or something?)

cd $mosesdir
mkdir $datadir
cd..
#units to moses...

popd