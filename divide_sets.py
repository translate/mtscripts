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

def divide(argv):
	corpuspath = argv[1]
	corpusdir, filename = os.path.split(corpuspath)
	lines = file(corpuspath).readlines()
	
	f = open(os.path.join(corpusdir,"tune_"+filename), 'w')
	f = open(os.path.join(corpusdir,"test_"+filename), 'w')
	f = open(os.path.join(corpusdir,"train_"+filename), 'w')
	
	t = 100
	num = len(lines) - t
	
	tune_set, test_set, train_set = lines[:t], lines[t:int(num*0.1)+t], lines[int(num*0.1)+t:]
	
	for l in tune_set:
		file(os.path.join(corpusdir,"tune_"+filename),'a').write(l)
	
	for l in test_set:
		file(os.path.join(corpusdir,"test_"+filename),'a').write(l)
	
	for l in train_set:
		file(os.path.join(corpusdir,"train_"+filename),'a').write(l)
	

if __name__ == "__main__":
	from sys import argv
	divide(argv)