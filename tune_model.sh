#!/bin/bash
# -*- coding: utf-8 -*-

workdir=work_2Aug
datadir=data_2Aug
tuningdir=tuning
testdir=test
evaldir=evaluation
corpusdir=corpus_2Aug
origcorpus=FINAL_CORPUS
traintag=train_
testtag=test_
tunetag=tune_
tu_corpusname=$tunetag$(echo corpus_2Aug)
te_corpusname=$testtag$(echo corpus_2Aug)

pushd .

echo "Removing any previous tuning sets with name "$workdir" or "$datadir"."
rm -r /home/laurette/Translate_org_za/Moses/$datadir/$tuningdir
mkdir /home/laurette/Translate_org_za/Moses/$datadir/$tuningdir
mkdir /home/laurette/Translate_org_za/Moses/$datadir/$testdir
cp $origcorpus/$tunetag* /home/laurette/Translate_org_za/Moses/$datadir/$tuningdir
cp $origcorpus/$testtag* /home/laurette/Translate_org_za/Moses/$datadir/$testdir

cd /home/laurette/Translate_org_za/Moses
mkdir $workdir/$tuningdir
tools/scripts/tokenizer.perl -l zu < $datadir/$tuningdir/$tu_corpusname.zu > $workdir/$tuningdir/$tu_corpusname.tok.zu
tools/scripts/tokenizer.perl -l xh < $datadir/$tuningdir/$tu_corpusname.xh > $workdir/$tuningdir/$tu_corpusname.tok.xh
mkdir $workdir/$evaldir
tools/scripts/tokenizer.perl -l zu < $datadir/$testdir/$te_corpusname.zu > $workdir/$evaldir/$corpusname.tok.zu

nohup nice tools/moses-scripts/scripts-20110627-1042/training/mert-moses.pl $workdir/$tuningdir/$tu_corpusname.tok.zu $workdir/$tuningdir/$tu_corpusname.tok.xh tools/moses/moses-cmd/src/moses $workdir/model/moses.ini --working-dir $workdir/$tuningdir/mert --mertdir /home/laurette/Translate_org_za/Moses/tools/moses/mert --rootdir /home/laurette/Translate_org_za/Moses/tools/moses-scripts/scripts-20110627-1042/ --decoder-flags "-v 0" >& $workdir/$tuningdir/mert.out

popd
