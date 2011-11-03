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

POL_THRESHOLD = 0.25

#TODO: decide what to do with single quotes, since they sometimes appear as part of a word
punct = re.compile(u'([.]|,|\?|!|:|;|\'|"|“|”|‘|’|—|\)|\()') #might need expanding
spaces = re.compile('\s+') #reduces any amount of successive whitespace to one space character

def spellcheck_filter(line, filters):
    if line:
        import enchant        
        words = line.split()
        pollution = 0.0
        for w in words:
            for f in filters:
                if f != '-':
                    try:
                        d = enchant.Dict(f)
                        if d.check(w):
                            pollution = pollution + 1
                            break #increment pollution if word matches at least one filter
                    except enchant.DictNotFoundError:
                        print "Dictionary",f,"not found, skipping..."
                        continue
        if len(words)> 0 and pollution/len(words) < POL_THRESHOLD:
                return line
        else:
            return None
    return line

def segment_units(corpus):
    from translate.tools import posegment
    from translate.lang import factory
    sourcelang = factory.getlanguage("en")
    targetlang = factory.getlanguage("af")
    seg = posegment.segment(sourcelang, targetlang)
    return seg.convertstore(corpus)

def fix_unit(u, cleanup, filters):
    if cleanup:
        if u.source:
            u.source = cleanup(u.source)
        if u.target:
            u.target = cleanup(u.target)
    if filters:
        u.source = spellcheck_filter(u.source, filters)
        u.target = spellcheck_filter(u.target, filters)
    if u.source:
        u.source = fix_punct(u.source.lower())
    if u.target:
        u.target = fix_punct(u.target.lower())
    
    return u

def fix_punct(ustr): #pretends that abbreviations don't exist
    global punct
    if ustr:
        nstr = punct.sub(u' \g<1> ', ustr)
        mstr = spaces.sub(' ', nstr)
        return mstr.strip()
    return None

def write_units(corpusname, mono, lang1=u"", lang2=u"", enc='utf-8', units=[], outdir=None):
    print len(units)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    s = codecs.open(os.path.join(outdir,corpusname + u"." + lang1), 'a', enc)
    #random.shuffle(units)
    
    if mono:
        sources = [unicode(str(u.source).strip() +"\n", enc) for u in units if not u.isheader()]
        for l in sources:
            s.write(l)
        s.close()
    
    else:
        sources = [unicode(str(u.source).strip() +"\n", enc) for u in units if u.istranslated()]
        for l in sources:
            s.write(l)
        s.close()
        t = codecs.open(os.path.join(outdir,corpusname + u"." + lang2), 'a', enc)
        targets = [unicode(str(u.target).strip() +"\n", enc) for u in units if u.istranslated()]
        for l in targets:
            t.write(l)
        t.close()

def create_option_parser():
    """Creates command-line option parser for when this script is used on the
        command-line. Run "corpus_collect.py -h" for help regarding options."""
    from optparse import OptionParser
    usage='Usage: %prog [<options>] <language tag 1> <language tag 2> <bilingual files>'
    parser = OptionParser(usage=usage)

    parser.add_option(
        '-o', '--output-dir',
        dest='outputdir',
        help=_('Output directory to use. Default: location of input file.'),
        default='output'
    )
    parser.add_option(
        '-c', '--cleaner',
        dest='cleaner',
        choices = ["cleaner","daccleaner","webcleaner"],
        help=_('Specify the module to be used for cleaning.'),
        default=None
    )
    parser.add_option(
        '-s', '--segment',
        dest='segment',
        help=_('Option to perform posegment on po files.'),
        action='store_true',
        default=False
    )    
    parser.add_option(
        '-n', '--corpus_name',
        dest='corpusname',
        help=_('Specify corpus name.'),
        default='corpus'
    )
    parser.add_option(
        '-l', '--lang-filter',
        dest='filters',
        nargs=4,
        help=('Specify language tags of lines to be removed. Exactly four tags must be given, use - for empty tags.'),
        default=None
    )
    parser.add_option(
        '-f', '--filenames',
        dest='filenames',
        help=('Specify a file containing a list of names of files to be converted.'),
        default=None
    )
    parser.add_option(
        '-m', '--mono',
        dest='mono',
        action='store_true',
        help=('Indicate that input is monolingual: only one output file results.'),
        default=False
    )
    return parser

if __name__ == "__main__":
    """Usage: corpusfile lang1 lang2"""
    
    options, args = create_option_parser().parse_args()
    
    corpusname = options.corpusname
    outdir = options.outputdir
    cleanerchoice = options.cleaner #change to accommodate changes to cleaners...
    filters = options.filters
    mono = options.mono
    filenames = options.filenames
    segment = options.segment

    import cleaner
    import daccleaner
    import webcleaner
    
    cleaners = {
                "cleaner":cleaner.Cleaner(),
                "daccleaner":daccleaner.DACCleaner(),
                "webcleaner":webcleaner.WebCleaner()
               }

    if cleanerchoice:
        cleaner = cleaners[cleanerchoice]
        cleanup = cleaner.cleanup
    else:
        cleanup = None
    
    #remove previous contents of corpus
    if len(args) >= 2:
        try:
            s = codecs.open(os.path.join(outdir,corpusname + u"." + args[0]), 'w', 'utf-8')
            s.close()
        except IOError:
            print "No file",corpusname+"."+args[0],"to be removed"
        try:
            t = codecs.open(os.path.join(outdir,corpusname + u"." + args[1]), 'w', 'utf-8')
            t.close()
        except IOError:
            print "No file",corpusname+"."+args[1],"to be removed"
    
    #if filesnames are to be read from a file
    if len(args) == 2:
        lang1 = args[0]
        lang2 = args[1]
        if filenames:
            n = codecs.open(filenames,'r','utf-8')
            lines = n.readlines()
            for l in lines:
                try:
		    corpus = factory.getobject(l[:-1])
                    print l,": ",len(corpus.units)
		    if segment:
                        corpus = segment_units(corpus)    
                    for u in corpus.units:
                        fix_unit(u, cleanup, filters)
                    write_units(corpusname, mono, lang1, lang2, 'utf-8', corpus.units, outdir)
                except ValueError, e:
                    print e,"Could not convert "+l+" to factory."
                    continue
    
    #if filenames are given as paramaters
    elif len(args) >= 2:
        lang1 = args[0]
        lang2 = args[1]
        files = []
        for f in args[2:]:
            if os.path.exists(f):
                if os.path.isdir(f):
                    for fn in os.listdir(f):
                        if fn.endswith('.txt') and not os.path.isdir(fn):
                            files.append(os.path.join(f, fn))
                else:
                    files.append(f)
        for f in files:
            try:
                corpus = factory.getobject(f)
                print f,": ",corpus.units
		if segment:
                    units = segment_units(corpus)
                for u in corpus.units:
                    fix_unit(u, cleanup, filters)
                write_units(corpusname, mono, lang1, lang2, 'utf-8', corpus.units, outdir)
            except ValueError:
                print "Could not convert "+f+" to factory."
                continue

        if not files:
            print 'No input files specified.'
            exit(1)
        
    else:
        print "Usage: %prog [<options>] <language 1> <language 2> <bilingual files>"
        exit()
