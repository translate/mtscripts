#!/bin/bash
# -*- coding: utf-8 -*-

aligneddir=aligned.po-files
translateddir=translated.po-files
podir=PO-FILES
corpusdir=CORPUS
finaldir=FINAL_CORPUS
corpusname=corpus_2Aug

srclang=zu
tgtlang=xh

# Retrieve latest corpus data from indlovu
#   1. Reviewed alignment .po files
#   2. Translated .po files

ssh indlovu.local /var/samba/public/mt-work/alignment/copy_po.sh
scp -r indlovu.local:/var/samba/public/mt-work/alignment/$aligneddir /home/laurette/Translate_org_za/Moses_scripting

ssh indlovu.local /var/samba/public/mt-work/translations/copy_po.sh
scp -r indlovu.local:/var/samba/public/mt-work/translations/$translateddir /home/laurette/Translate_org_za/Moses_scripting

mkdir $podir
cp $aligneddir/* $podir
cp $translateddir/* $podir
#rm -r $aligneddir
#rm -r $translateddir

# Convert to Moses corpus

#sh get_moses_format.sh $srclang $tgtlang $podir $corpusdir $corpusname $finaldir

# Divide into training, tuning and test sets
#~ for c in $(cd $finaldir; ls $corpusname*)
#~ do
	#~ echo $c
	#~ python divide_sets.py $finaldir/$c
#~ done
