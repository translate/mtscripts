#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Input: directory with sub-directories containing po files
# Output: file containing random, proportionate sample of data by sub-directory
# By-product: A tmx file for each sub-directory

import os
from translate.tools import pomerge

def create_file(dir):
	dirpath = os.path.abspath(dir)
	from translate.convert import po2tmx
	po2tmx.main(["--language=xh","--input="+dirpath, "--output="+dirpath+".tmx"])

def create_intermediates(dir):
	#from translate.convert import tmx2po
	for e in os.listdir(dir):
		if os.path.isdir(os.path.join(dir,e)):
			create_file(os.path.join(dir,e))
			#tmx2po.converttmx(os.path.join(os.path.join(dir,e)))

def create_sample(unitslist, percentage):
	import random
	outlist = []
	for l in unitslist:
		random.shuffle(l)
		outlist.append(l[:int(len(l)*percentage)])
	return outlist

def create_option_parser():
    """Creates command-line option parser for when this script is used on the
        command-line. Run "corpus_collect.py -h" for help regarding options."""
    from optparse import OptionParser
    usage='Usage: %prog [<options>] <input dir> <output file>'
    parser = OptionParser(usage=usage)

    parser.add_option(
        '-s', '--sample',
        dest='percentage',
        help=('Specify a percentage to be output as a sample.'),
        default=1
    )
    return parser

def main(dir, output, pstr):
	
	import random
	percentage = float(pstr)
	from translate.storage import factory
	unitslist = []
	create_intermediates(dir)
	
	print "Creating final TMX..."
	for f in os.listdir(dir):
		if f.endswith(".tmx") and not os.path.isdir(f):
			try:
				filepath = os.path.join(dir,f)
				minicorpus = factory.getobject(filepath)
				for u in minicorpus.units:
					u.addnote("Origin: "+f)
				unitslist.append(minicorpus.units)
			except ValueError:
				print "Could not convert to factory."
				continue
	
	sample_list = create_sample(unitslist, percentage)
	sample = []
	for l in sample_list:
		sample.extend(l)
	random.shuffle(sample)
	
	if os.path.exists(output):
		os.remove(output)
	newcorpus = factory.getobject(output)
	for u in sample:
		newunit = newcorpus.UnitClass.buildfromunit(u)
		newcorpus.addunit(newunit)
	newcorpus.save()

if __name__ == "__main__":
	
	options, args = create_option_parser().parse_args()
	
	percentage = options.percentage
	if len(args) == 2:
		main(args[0], args[1], percentage)
	else:
		print "Usage: python get_random_sample.py [<options>] <input dir> <output file>"