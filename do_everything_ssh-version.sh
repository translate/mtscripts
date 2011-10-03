#!/bin/bash

#need to find a way (ssh-keygen?) to prevent the password typing annoyance

pushd .

translations=false
alignment=false

if [ "$1" = "t" ]; then
	translations=true
	if [ "$2" = "a" ]; then
		alignment=true
	fi
else echo 'USAGE: ./do_everything_ssh-version.sh [t] [a]'; exit
fi

if [ "$1" = "a" ]; then
	alignment=true
fi

langtag1='zu'
langtag2='xh'
corpusname='corpus'
datadir='data'
mosesdir='moses'
#podir='po-files'
transdir='po-translations'
aligndir='po-alignments'
segtransdir='seg-translations'

mkdir $datadir
cd $datadir
#mkdir $podir
mkdir $transdir
mkdir $segtransdir
mkdir $aligndir
cd ..

server='indlovu.local'
transservpath='/var/samba/public/mt-work/translations'
alignservpath='/var/samba/public/mt-work/alignment'
servdir='4.reviewed'
locpath='/home/laurette/Translate_org_za/trunk/mtscripts'

if $translations ; then
	echo 'Downloading translations'
	sh download.sh $server $transservpath $servdir $locpath $transdir $datadir
fi

if $alignment ; then
	echo 'Downloading alignment'
	sh download.sh $server $alignservpath $servdir $locpath $aligndir $datadir
fi

echo $(pwd)

#segment_po.py to segment translations

if $translations ; then
	python segment_po.py $datadir/$transdir $datadir/$segtransdir
	echo 'Performing pocount: translations'
	pocount $datadir/$segtransdir/* | tail -n 9 > pocount_translations
fi

#pocounts for alignment and translations

if $alignment ; then
	echo 'Performing pocount: alignment'
	pocount $datadir/$aligndir/* | tail -n 9 > pocount_alignment
fi

mkdir $mosesdir
cd $mosesdir
mkdir pofiles
mkdir mosesformat
mkdir corpus
cd ..

echo "Copying all .po files into $mosesdir/pofiles"
if $translations ; then
	cp $datadir/$segtransdir/* $mosesdir/pofiles
fi
if $alignment ; then
	cp $datadir/$aligndir/* $mosesdir/pofiles
fi

echo 'Converting .po files to moses format...'
#make individual moses format files, then concatenate

python units_to_moses.py -c -n $corpusname -o $mosesdir/mosesformat $langtag1 $langtag2 $(ls $mosesdir/pofiles/*.po)

cd $mosesdir/mosesformat
echo 'Catenating all moses format files'
cat $(ls *.$langtag1) > ../corpus/$corpusname.$langtag1
cat $(ls *.$langtag2) > ../corpus/$corpusname.$langtag2

popd