#!/bin/bash

# Builds corpus from bilingual files
# Builds a Moses model from the corpus

pushd .

. variables.sh

# 0. Prepare folders for downloading data

echo "Creating data folder"
mkdir $datadir

# 1. Download data from server or copy from file system

if $useserver; then
	for i in "${servpaths[@]}"
	do
		echo "Download from $i:"
		scp -r $server:$i/* $locpath/$datadir
	done
else for i in "${srcpaths[@]}"
	do
		echo "Copying from $i..."
		cp -r $i/* $locpath/$datadir
	done
fi

# 2. Segment data

if $posegment ; then
	posegment $datadir $segmentdir
	datadir=$segmentdir
fi

# 3. Write pocounts for data

if $pocount ; then
	echo 'Performing pocount'
	pocount $datadir | tail -n 9 > pocount 
fi

# 4. Convert data to Moses format
if $mosesconvert; then
	mkdir $mosesdir
	echo 'Converting files to moses format...'
	python units_to_moses.py -c -n $corpusname -o $mosesdir $langtag1 $langtag2 $(find $datadir -type f)
fi

# 5. Build a Moses model

if $buildmodel; then
	sh build_model.sh
fi


popd