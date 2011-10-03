#!/bin/bash
# -*- coding: utf-8 -*-

pushd .

mosespath='/home/laurette/Translate_org_za/Moses'
workdir=work_3Oct
datadir=data_3Oct
corpuspath='/home/laurette/Translate_org_za/trunk/mtscripts/moses/corpus'
corpusname=corpus
traintag=train_
testtag=test_
tunetag=tune_
traincorpus=$traintag$(echo $corpusname)
testcorpus=$testtag$(echo $corpusname)
tunecorpus=$tunetag$(echo $corpusname)

cd $mosespath
echo "Removing any previous models with name "$workdir" or "$datadir"."
rm -r $datadir
mkdir $datadir
cp $corpuspath/$corpusname* $datadir

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

nohup nice $mosespath/tools/moses-scripts/scripts-20110627-1042/training/train-model.perl -scripts-root-dir $mosespath/tools/moses-scripts/scripts-20110627-1042/ -root-dir $workdir -corpus $workdir/$corpusname/$corpusname.clean -f zu -e xh -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:$mosespath/$workdir/lm/$corpusname.lm >& $workdir/training.out

popd