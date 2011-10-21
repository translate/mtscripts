#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, glob, os

def rename(files, pattern, replacement):
	for pathname in glob.glob(files):
		basename = os.path.basename(pathname)
		new_filename = re.sub(pattern, replacement, basename)
		if new_filename != basename:
			print "Renaming", basename, "-->", new_filename
			os.rename(pathname, os.path.join(os.path.dirname(pathname), new_filename))

if __name__ == "__main__":
	from sys import argv
	try:
		rename(argv[1], argv[2], argv[3])
	except IndexError:
		print "Usage: python rename \"<files>\" <pattern> <replacement>"