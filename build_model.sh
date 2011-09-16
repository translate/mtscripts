#!/bin/bash
# -*- coding: utf-8 -*-

workdir=work_2Aug
datadir=data_2Aug
corpusdir=corpus_2Aug
origcorpus=FINAL_CORPUS
traintag=train_
testtag=test_
tunetag=tune_
corpusname=$traintag$(echo corpus_2Aug)

echo "Removing any previous models with name "$workdir" or "$datadir"."
rm -r /home/laurette/Translate_org_za/Moses/$datadir
mkdir /home/laurette/Translate_org_za/Moses/$datadir
cp $origcorpus/$traintag* /home/laurette/Translate_org_za/Moses/$datadir
cd /home/laurette/Translate_org_za/Moses

rm -r $workdir
mkdir $workdir
mkdir $workdir/$corpusdir

tools/scripts/tokenizer.perl -l zu < $datadir/$corpusname.zu > $workdir/$corpusdir/$corpusname.tok.zu
tools/scripts/tokenizer.perl -l xh < $datadir/$corpusname.xh > $workdir/$corpusdir/$corpusname.tok.xh

tools/moses-scripts/scripts-20110627-1042/training/clean-corpus-n.perl $workdir/$corpusdir/$corpusname.tok zu xh $workdir/$corpusdir/$corpusname.clean 1 40

mkdir $workdir/lm
cp $workdir/$corpusdir/$corpusname.tok.xh $workdir/lm/$corpusname.xh
#^^ This is where monolingual data should be added too

tools/srilm/bin/i686-ubuntu/ngram-count -order 3 -interpolate -kndiscount -unk -text $workdir/lm/$corpusname.xh -lm $workdir/lm/$corpusname.lm

nohup nice tools/moses-scripts/scripts-20110627-1042/training/train-model.perl -scripts-root-dir tools/moses-scripts/scripts-20110627-1042/ -root-dir $workdir -corpus $workdir/$corpusdir/$corpusname.clean -f zu -e xh -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/home/laurette/Translate_org_za/Moses/$workdir/lm/$corpusname.lm >& $workdir/training.out
