#!/bin/bash
# -*- coding: utf-8 -*-

pushd .

. variables.sh

cd $mosespath
echo "Removing any previous models with name "$bworkdir" or "$bdatadir"."
rm -r $bdatadir
mkdir $bdatadir
mkdir $bdatadir/tuning
mkdir $bdatadir/evaluation
cp $corpuspath/$corpusname* $bdatadir
cp $corpuspath/$tunetag$corpusname* $bdatadir/tuning
cp $corpuspath/$testtag$corpusname* $bdatadir/evaluation

rm -r $bworkdir
mkdir $bworkdir
mkdir $bworkdir/$corpusname

$mosespath/tools/scripts/tokenizer.perl -l zu < $bdatadir/$corpusname.zu > $bworkdir/$corpusname/$corpusname.tok.zu
$mosespath/tools/scripts/tokenizer.perl -l xh < $bdatadir/$corpusname.xh > $bworkdir/$corpusname/$corpusname.tok.xh

$mosespath/tools/moses-scripts/scripts-20110627-1042/training/clean-corpus-n.perl $bworkdir/$corpusname/$corpusname.tok zu xh $bworkdir/$corpusname/$corpusname.clean 1 40

mkdir $bworkdir/lm
cp $bworkdir/$corpusname/$corpusname.tok.xh $bworkdir/lm/$corpusname.xh
#^^ This is where monolingual data should be added too

$mosespath/tools/srilm/bin/i686-ubuntu/ngram-count -order 3 -interpolate -kndiscount -unk -text $bworkdir/lm/$corpusname.xh -lm $bworkdir/lm/$corpusname.lm

echo 'Building model'
nohup nice $mosespath/tools/moses-scripts/scripts-20110627-1042/training/train-model.perl -scripts-root-dir $mosespath/tools/moses-scripts/scripts-20110627-1042/ -root-dir $bworkdir -corpus $bworkdir/$corpusname/$corpusname.clean -f zu -e xh -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:$mosespath/$bworkdir/lm/$corpusname.lm >& $bworkdir/training.out

mkdir $bworkdir/tuning
$mosespath/tools/scripts/tokenizer.perl -l zu < $bdatadir/tuning/$tunetag$corpusname.zu > $bworkdir/tuning/$tunetag$corpusname.tok.zu
$mosespath/tools/scripts/tokenizer.perl -l xh < $bdatadir/tuning/$tunetag$corpusname.xh > $bworkdir/tuning/$tunetag$corpusname.tok.xh

mkdir $bworkdir/evaluation
$mosespath/tools/scripts/tokenizer.perl -l zu < $bdatadir/evaluation/$testtag$corpusname.zu > $bworkdir/evaluation/$testtag$corpusname.tok.zu

if $tuning; then
	echo 'Tuning model'
	nohup nice $mosespath/tools/moses-scripts/scripts-20110627-1042/training/mert-moses.pl $bworkdir/tuning/$tunetag$corpusname.tok.zu $bworkdir/tuning/$tunetag$corpusname.tok.xh $mosespath/tools/moses/moses-cmd/src/moses $bworkdir/model/moses.ini --working-dir $bworkdir/tuning/mert --mertdir $mosespath/tools/moses/mert --rootdir $mosespath/tools/moses-scripts/scripts-20110627-1042/ --decoder-flags "-v 0" >& $bworkdir/tuning/mert.out
fi

popd