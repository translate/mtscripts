#!/bin/bash
# -*- coding: utf-8 -*-

pushd .

. variables.sh

cd $mosespath
# if get data...
if $getdata ; then

    echo "Removing any previous data in "$bdatadir"."
    rm -r $bdatadir
    mkdir $bdatadir
    mkdir $bdatadir/tuning
    mkdir $bdatadir/evaluation
    cp $corpuspath/$corpusname* $bdatadir
    cp $corpuspath/$tunetag$corpusname* $bdatadir/tuning
    cp $corpuspath/$testtag$corpusname* $bdatadir/evaluation
fi

echo "Removing previous models with name "$bworkdir
rm -r $bworkdir
mkdir $bworkdir
mkdir $bworkdir/$corpusname

$mosespath/tools/scripts/tokenizer.perl -l $langtag1 < $bdatadir/$corpusname.$langtag1 > $bworkdir/$corpusname/$corpusname.tok.$langtag1
$mosespath/tools/scripts/tokenizer.perl -l $langtag2 < $bdatadir/$corpusname.$langtag2 > $bworkdir/$corpusname/$corpusname.tok.$langtag2

$mosespath/tools/moses-scripts/scripts-$installdate/training/clean-corpus-n.perl $bworkdir/$corpusname/$corpusname.tok $langtag1 $langtag2 $bworkdir/$corpusname/$corpusname.clean 1 40

mkdir $bworkdir/lm
cp $bworkdir/$corpusname/$corpusname.tok.$langtag2 $bworkdir/lm/$corpusname.$langtag2
#^^ This is where monolingual data should be added too

$mosespath/tools/srilm/bin/$system/ngram-count -order $order -interpolate -kndiscount -unk -text $bworkdir/lm/$corpusname.$langtag2 -lm $bworkdir/lm/$corpusname.lm

echo 'Building model'
nohup nice $mosespath/tools/moses-scripts/scripts-$installdate/training/train-model.perl -scripts-root-dir $mosespath/tools/moses-scripts/scripts-$installdate/ -root-dir $bworkdir -corpus $bworkdir/$corpusname/$corpusname.clean -f $langtag1 -e $langtag2 -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:$mosespath/$bworkdir/lm/$corpusname.lm >& $bworkdir/training.out

if $tuning; then
    mkdir $bworkdir/tuning
    $mosespath/tools/scripts/tokenizer.perl -l $langtag1 < $bdatadir/tuning/$tunetag$corpusname.$langtag1 > $bworkdir/tuning/$tunetag$corpusname.tok.$langtag1
    $mosespath/tools/scripts/tokenizer.perl -l $langtag2 < $bdatadir/tuning/$tunetag$corpusname.$langtag2 > $bworkdir/tuning/$tunetag$corpusname.tok.$langtag2
fi

if $testing ; then
    mkdir $bworkdir/evaluation
    $mosespath/tools/scripts/tokenizer.perl -l $langtag1 < $bdatadir/evaluation/$testtag$corpusname.$langtag1 > $bworkdir/evaluation/$testtag$corpusname.tok.$langtag1
fi

if $tuning; then
	echo 'Tuning model'
	nohup nice $mosespath/tools/moses-scripts/scripts-$installdate/training/mert-moses.pl $mosespath/$bworkdir/tuning/$tunetag$corpusname.tok.$langtag1 $mosespath/$bworkdir/tuning/$tunetag$corpusname.tok.$langtag2 $mosespath/tools/moses/moses-cmd/src/moses $mosespath/$bworkdir/model/moses.ini --working-dir $mosespath/$bworkdir/tuning/mert --mertdir $mosespath/tools/moses/mert --rootdir $mosespath/tools/moses-scripts/scripts-$installdate/ --decoder-flags "-v 0" >& $mosespath/$bworkdir/tuning/mert.out
fi

popd
