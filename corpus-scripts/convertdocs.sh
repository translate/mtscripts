#!/bin/bash

#pdfdir=paired-docs/PDF
worddir=isiXhosa

#python rename.py "$pdfdir/*.pdf" " " _
python rename.py "$worddir/*.doc*" " " _

for t in $(cd $pdfdir; ls *.pdf)
do
	filename=$(basename $t .pdf)
	echo "Converting" $pdfdir/$t
	jython convertpdf.py $pdfdir/$t > $pdfdir/$filename.txt
	
done

for t in $(cd $worddir; ls *.doc*)
do
	filename=$(basename $t)
	extension=${filename##*.}
	filename=${filename%.*}
	echo "Converting" $worddir/$t
	abiword --to=txt $worddir/$t
	
done