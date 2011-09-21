#!/bin/bash

#need to find a way (ssh-keygen?) to prevent the password typing annoyance

pushd .

langtag1='zu'
langtag2='xh'
corpusname='corpus'
datadir='data'
mosesdir='moses'
#podir='po-files'
alltransdir='po-translations'
allaligndir='po-alignments'
segtransdir='seg-translations'
mkdir $datadir
cd $datadir
#mkdir $podir
mkdir $alltransdir
mkdir $segtransdir
mkdir $allaligndir
cd ..

indpath='/var/samba/public/mt-work'
locpath='/home/laurette/Translate_org_za/trunk/mtscripts'
transdir='translations'
aligndir='alignment'

#echo $alltransdir
#scp -f copy_po.sh indlovu.local:$indpath/$transdir
#scp -f copy_po.sh indlovu.local:$indpath/$aligndir
ssh indlovu.local "cd $indpath/$transdir; sh copy_po.sh 4.reviewed $alltransdir"
scp indlovu.local:$indpath/$transdir/$alltransdir/* $locpath/$datadir/$alltransdir
ssh indlovu.local "cd $indpath/$aligndir; sh copy_po.sh 4.reviewed $allaligndir"
scp indlovu.local:$indpath/$aligndir/$allaligndir/* '/home/laurette/Translate_org_za/trunk/mtscripts/'$datadir/$allaligndir

#segment_po.py to segment translations

python segment_po.py $datadir/$alltransdir $datadir/$segtransdir

#pocounts for alignment and translations

echo 'Performing pocount: translations'
pocount $datadir/$segtransdir/* | tail -n 9 > pocount_translations
echo 'Performing pocount: alignment'
pocount $datadir/$allaligndir/* | tail -n 9 > pocount_alignment

mkdir $mosesdir
cd $mosesdir
mkdir pofiles
mkdir mosesformat
cd ..

echo "Copying all .po files into $mosesdir/pofiles"
cp $datadir/$segtransdir/* $mosesdir/pofiles
cp $datadir/$allaligndir/* $mosesdir/pofiles

echo 'Converting .po files to moses format...'
#make individual moses format files, then concatenate
for d in $(cd $mosesdir; ls)
do
	echo $d
	python units_to_moses.py -o $mosesdir/mosesformat $d $langtag1 $langtag2
done

echo 'Catenating all moses format files'
cd $mosesdir/mosesformat
cat $(ls *.$langtag1) > ../$corpusname.$langtag1
cat $(ls *.$langtag2) > ../$corpusname.$langtag2

popd