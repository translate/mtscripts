#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Zuza Software Foundation
#
# This file is part of translate.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import random
import os.path

def divide(args, tune, eval):
	corpuspath = args[0]
	corpusdir, filename = os.path.split(corpuspath)
	lines = file(corpuspath).readlines()
	tune_set = []
	test_set = []
	
	t = float(tune)
	e = float(eval)
	
	if t > 0 and t <= 1:
		#create/clear tuning file
		f = open(os.path.join(corpusdir,"tune_"+filename), 'w')
		tune_set = lines[:int(len(lines)*t)]
	
	if e > 0 and e <= 1:
		#create/clear testing file
		f = open(os.path.join(corpusdir,"test_"+filename), 'w')
		test_set = lines[int(len(lines)*t):int(len(lines)*t)+int(len(lines)*e)]
	
	f = open(os.path.join(corpusdir,"complete_"+filename), 'w')
	
	train_set = lines[int(len(lines)*t)+int(len(lines)*e):]
	
	for l in lines:
		file(os.path.join(corpusdir,"complete_"+filename),'a').write(l)
	
	for l in tune_set:
		file(os.path.join(corpusdir,"tune_"+filename),'a').write(l)
	
	for l in test_set:
		file(os.path.join(corpusdir,"test_"+filename),'a').write(l)
	
	f = open(os.path.join(corpusdir,filename), 'w')
	for l in train_set:
		file(os.path.join(corpusdir,filename),'a').write(l)

def create_option_parser():
    """Creates command-line option parser for when this script is used on the
        command-line. Run "corpus_collect.py -h" for help regarding options."""
    from optparse import OptionParser
    usage='Usage: %prog [<options>] <bilingual file> <language tag 1> <language tag 2>'
    parser = OptionParser(usage=usage)

    parser.add_option(
        '-u', '--create-tuning',
        dest='tuning',
        help='Specify percentage of corpus to be used for tuning corpus.',
        default=0
    )
    parser.add_option(
        '-e', '--create-evaluation',
        dest='eval',
        help='Specify percentage of corpus to be used for tuning corpus.',
        default=0
    )
    return parser

if __name__ == "__main__":
	
	options, args = create_option_parser().parse_args()
	if len(args) >= 1:
		divide(args, options.tuning, options.eval)
	else:
		print "Usage: %prog [<options>] <corpus file>"
	