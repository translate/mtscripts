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

from translate.storage import factory
from translate.tools import posegment
import os
from gettext   import gettext as _
import re
import random
import codecs
import cleaner

#TODO: decide what to do with single quotes, since they sometimes appear as part of a word
punct = re.compile(u'([.]|,|\?|!|:|;|\'|"|“|”|‘|’|—|\)|\()') #might need expanding
spaces = re.compile('\s+') #reduces any amount of successive whitespace to one space character


def write_corpusfiles(corpusname, lang1=u"", lang2=u"", enc='utf-8', lunits=[], clean=False, outdir=None):
    
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    s = codecs.open(os.path.join(outdir,corpusname + u"." + lang1), 'w', enc)
    t = codecs.open(os.path.join(outdir,corpusname + u"." + lang2), 'w', enc)
    random.shuffle(lunits)
    
    for u in lunits:
        if clean:
            if u.istranslated():
                srcstr = fix_punct(cleaner.cleanup(u.source)) 
                tgtstr = fix_punct(cleaner.cleanup(u.target))
                # If either srcstr or tgtstr are None, do not write the unit
                if not (srcstr == None or tgtstr == None):
                    s.write(srcstr.lower() + u"\n")
                    t.write(tgtstr.lower() + u"\n")
        else:
            if u.istranslated():
                srcstr = fix_punct(u.source) 
                tgtstr = fix_punct(u.target)
                if not (srcstr == None or tgtstr == None):
                    s.write(srcstr.lower() + u"\n")
                    t.write(tgtstr.lower() + u"\n")
    s.close()
    t.close()
    
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
    usage='Usage: %prog [<options>] <bilingual file> <language tag 1> <language tag 2>'
    parser = OptionParser(usage=usage)

    parser.add_option(
        '-o', '--output-dir',
        dest='outputdir',
        help=_('Output directory to use. Default: location of input file.'),
        default=None
    )
    parser.add_option(
        '-s', '--segmented-output-dir',
        dest='segoutdir',
        help=_('Output directory to use for segmented files.'),
        default='segmented'
    )
    parser.add_option(
        '-c', '--clean',
        dest='usecleaner',
        action='store_true',
        help=_('Use the cleaner designed for our specific Zulu-Xhosa corpus.'),
        default=False
    )
    parser.add_option(
        '--skip-po-segmentation',
        dest='skipsegment',
        action='store_true',
        help=_('Skip segmentation of PO files.'),
        default=False
    )
    return parser

if __name__ == "__main__":
    """Usage: corpusfile lang1 lang2"""
    
    options, args = create_option_parser().parse_args()
    
    outdir = options.outputdir
    usecleaner = options.usecleaner
    skipsegment = options.skipsegment
    segoutdir = options.segoutdir
    
    if len(args) == 3:
        filepath = args[0]
        lang1 = args[1]
        lang2 = args[2]
    else:
        print "Usage: %prog [<options>] <bilingual file> <language 1> <language 2>"
        exit()
    
    if not outdir:
        outdir = os.path.split(filepath)[0]
    
    filename = os.path.split(filepath)[1]
    print "Converting", filename
    
    if filename.endswith('.po') and not skipsegment:
        if not os.path.exists(segoutdir):
            os.mkdir(segoutdir)
        outfile = os.path.join(segoutdir,filename)
        result = posegment.segmentfile(filepath,file(outfile,'w'),None)
        corpus = factory.getobject(outfile)
    else:
        corpus = factory.getobject(filename)
    
    import locale
    enc = locale.getpreferredencoding()
    corpusname = filename[:filename.rfind(u".")]
    
    write_corpusfiles(corpusname, lang1, lang2, enc, corpus.units, outdir=outdir)