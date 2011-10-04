#!/bin/bash

pushd .

. variables.sh

# 0. Prepare folders for downloading data

mkdir $datadir

# 1. Download data from server

if $useserver; then
	for i in "${servpaths[@]}"
	do
		echo "Download from $i"
		#sh download.sh $server $i $locpath $datadir $filetype
		scp -r $server:$i/* $locpath/$datadir
	done
# else copy from other files specified...
fi

# 2. Segment data

if $segment ; then
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


popd