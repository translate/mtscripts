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

POL_THRESHOLD = 0.25

from translate.storage import factory
from translate.tools import posegment
import os
from gettext   import gettext as _
import re
import random
import codecs

#TODO: decide what to do with single quotes, since they sometimes appear as part of a word
punct = re.compile(u'([.]|,|\?|!|:|;|\'|"|“|”|‘|’|—|\)|\()') #might need expanding
spaces = re.compile('\s+') #reduces any amount of successive whitespace to one space character

def filter_lines_spellcheck(units=[], lang_id=u""):
    newunits = []
    import enchant
    us = enchant.Dict("en_US")
    gb = enchant.Dict("en_GB")
    
    for u in units:
        src_words = u.source.split()
        print src_words
        src_pollution = 0.0
        for w in src_words:
            if us.check(w) or gb.check(w):
                src_pollution = src_pollution + 1
        
        if len(src_words)> 0 and src_pollution/len(src_words) < POL_THRESHOLD:
            newunits.append(u)
            
    return newunits

def write_corpusfiles(corpusname, enc='utf-8', lunits=[], clean=False, outdir=None, filter=None):
    
    print len(lunits)
    
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    s = codecs.open(os.path.join(outdir,u"cleaned-"+corpusname), 'w', enc)
    #random.shuffle(lunits)
    
    if filter:
        lunits = filter_lines_spellcheck(lunits, filter)
    
    for u in lunits:
        if clean:
            import dac_cleaner
            srcstr = fix_punct(u.source)
            srcstr = fix_punct(dac_cleaner.cleanup(u.source))
            if not (srcstr == None):
                s.write(srcstr.lower() + u"\n")
        else:
            srcstr = fix_punct(u.source) 
            if not (srcstr == None):
                s.write(srcstr + u"\n")
    s.close()
    
def fix_punct(ustr): #pretends that abbreviations don't exist
    global punct
    if ustr:
        nstr = punct.sub(u' \g<1> ', ustr)
        mstr = spaces.sub(' ', nstr)
        return mstr.strip()
    return None

def create_option_parser():
    """Creates command-line option parser for when this script is used on the
        command-line. Run "corpus_collect.py -h" for help regarding options."""
    from optparse import OptionParser
    usage='Usage: %prog [<options>] <monolingual files>'
    parser = OptionParser(usage=usage)

    parser.add_option(
        '-o', '--output-dir',
        dest='outputdir',
        help=_('Output directory to use. Default: location of input file.'),
        default='output'
    )
    parser.add_option(
        '-c', '--clean',
        dest='usecleaner',
        action='store_true',
        help=_('Use the cleaner designed for our specific Zulu-Xhosa corpus.'),
        default=False
    )
    parser.add_option(
        '-n', '--corpus_name',
        dest='corpusname',
        help=_('Specify corpus name.'),
        default='corpus'
    )
    parser.add_option(
        '-f', '--filter-lang',
        dest='filter',
        help=_('Specify a language tag by which to filter lines.'),
        default=None
    )
    return parser

if __name__ == "__main__":
    """Usage: corpusfile lang1 lang2"""
    
    options, args = create_option_parser().parse_args()
    
    corpusname = options.corpusname
    outdir = options.outputdir
    usecleaner = options.usecleaner
    filter = options.filter
    
    if len(args) >= 1:
        files = []
        for f in args:
            if os.path.exists(f):
                if os.path.isdir(f):
                    for fn in os.listdir(f):
                        if fn.endswith('.txt') and not os.path.isdir(fn):
                            files.append(os.path.join(f, fn))
                else:
                    files.append(f)

        if not files:
            print 'No input files specified.'
            exit(1)
        
    else:
        print "Usage: python units_to_mono.py [<options>] <monolingual files>"
        exit()
    
    units = []
    for f in files:
        try:
            corpus = factory.getobject(f)
        except ValueError:
            print "Could not convert to factory."
            continue
        units.extend(corpus.units)
    
    import locale
    enc = locale.getpreferredencoding()
    
    write_corpusfiles(corpusname, enc, units, clean=usecleaner, outdir=outdir, filter=filter) #