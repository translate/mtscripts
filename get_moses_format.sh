#!/bin/bash
# -*- coding: utf-8 -*-

# Uses retag_lang, an awk file, and units_to_moses.py
# Creates a $corpusdir directory containing data from split tmx files.
# Then the data in $corpusdir is cleaned and stored in %cleandir.
# Meanwhile, the tmx files are retagged for language, renamed and stored in $retagdir.
# All cleaned data is then consolidated into two files and stored in $finaldir.


srclang=$1
tgtlang=$2
podir=$3
corpusdir=$4
corpusname=$5
finaldir=$6

cp units_to_moses.py ./$podir
cp cleaner.py ./$podir

mkdir -p $corpusdir
mkdir -p $finaldir

cd $podir
for t in $(ls *.po)
do
	python units_to_moses.py $t $srclang $tgtlang
	mv *.$srclang ../$corpusdir
	mv *.$tgtlang ../$corpusdir
done

cd ../$corpusdir
echo "Creating corpus from .po files"
cat *.$srclang > ../$finaldir/$corpusname.$srclang
cat *.$tgtlang > ../$finaldir/$corpusname.$tgtlang

cd ../$podir
cp units_to_moses.py ..
cp cleaner.py ..

