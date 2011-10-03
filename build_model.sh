#!/bin/bash
# -*- coding: utf-8 -*-

pushd .

mosespath='/home/laurette/Translate_org_za/Moses'
workdir=work_3Oct_t
datadir=data_3Oct_t
corpuspath='/home/laurette/Translate_org_za/trunk/mtscripts/moses/corpus'
corpusname=tcorpus
tunetag=tune_
tunecorpus=$tunetag$(echo $corpusname)
testtag=test_
testcorpus=$testtag$(echo $corpusname)

cd $mosespath
echo "Removing any previous models with name "$workdir" or "$datadir"."
rm -r $datadir
mkdir $datadir
mkdir $datadir/tuning
mkdir $datadir/evaluation
cp $corpuspath/$corpusname* $datadir
cp $corpuspath/$tunetag$corpusname* $datadir/tuning
cp $corpuspath/$testtag$corpusname* $datadir/evaluation

rm -r $workdir
mkdir $workdir
mkdir $workdir/$corpusname

$mosespath/tools/scripts/tokenizer.perl -l zu < $datadir/$corpusname.zu > $workdir/$corpusname/$corpusname.tok.zu
$mosespath/tools/scripts/tokenizer.perl -l xh < $datadir/$corpusname.xh > $workdir/$corpusname/$corpusname.tok.xh

$mosespath/tools/moses-scripts/scripts-20110627-1042/training/clean-corpus-n.perl $workdir/$corpusname/$corpusname.tok zu xh $workdir/$corpusname/$corpusname.clean 1 40

mkdir $workdir/lm
cp $workdir/$corpusname/$corpusname.tok.xh $workdir/lm/$corpusname.xh
#^^ This is where monolingual data should be added too

$mosespath/tools/srilm/bin/i686-ubuntu/ngram-count -order 3 -interpolate -kndiscount -unk -text $workdir/lm/$corpusname.xh -lm $workdir/lm/$corpusname.lm

echo 'Building model'
nohup nice $mosespath/tools/moses-scripts/scripts-20110627-1042/training/train-model.perl -scripts-root-dir $mosespath/tools/moses-scripts/scripts-20110627-1042/ -root-dir $workdir -corpus $workdir/$corpusname/$corpusname.clean -f zu -e xh -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:$mosespath/$workdir/lm/$corpusname.lm >& $workdir/training.out

mkdir $workdir/tuning
$mosespath/tools/scripts/tokenizer.perl -l zu < $datadir/tuning/$tunetag$corpusname.zu > $workdir/tuning/$tunetag$corpusname.tok.zu
$mosespath/tools/scripts/tokenizer.perl -l xh < $datadir/tuning/$tunetag$corpusname.xh > $workdir/tuning/$tunetag$corpusname.tok.xh

mkdir $workdir/evaluation
$mosespath/tools/scripts/tokenizer.perl -l zu < $datadir/evaluation/$testtag$corpusname.zu > $workdir/evaluation/$testtag$corpusname.tok.zu

echo 'Tuning model'
nohup nice $mosespath/tools/moses-scripts/scripts-20110627-1042/training/mert-moses.pl $workdir/tuning/$tunetag$corpusname.tok.zu $workdir/tuning/$tunetag$corpusname.tok.xh $mosespath/tools/moses/moses-cmd/src/moses $workdir/model/moses.ini --working-dir $workdir/tuning/mert --mertdir $mosespath/tools/moses/mert --rootdir $mosespath/tools/moses-scripts/scripts-20110627-1042/ --decoder-flags "-v 0" >& $workdir/tuning/mert.out

popd