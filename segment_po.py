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

from translate.tools import posegment
import os

def create_option_parser():
	"""Creates command-line option parser for when this script is used on the
		command-line. Run "corpus_collect.py -h" for help regarding options."""
	from optparse import OptionParser
	usage='Usage: %prog [<options>] <po directory> <output dir>'
	parser = OptionParser(usage=usage)
	
	return parser

if __name__ == "__main__":
	"""Usage: corpusfile lang1 lang2"""
	
	options, args = create_option_parser().parse_args()
	
	if len(args) == 2:
		indir = args[0]
		outdir = args[1]
	
	else:
		print "Usage: %prog [<options>] <po directory> <output dir>"
		exit()
	
	#if not outdir:
	#	outdir = os.join(os.path.split(filepath)[0],"output")
	import locale
	enc = locale.getpreferredencoding()
	
	files = os.listdir(indir)
	
	for f in files:
		if f.endswith('.po'):
			infile = os.path.join(indir,f)
			outfile = os.path.join(outdir,f)
			print outfile
			result = posegment.segmentfile(infile,file(outfile,'w'),None)