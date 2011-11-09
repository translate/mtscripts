#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Zuza Software Foundation
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

# """ TODO: doctsring

from translate.storage import factory
from translate.tools import posegment
import os
from gettext   import gettext as _
import re
import random
import codecs

POLLUTION_THRESHOLD = 0.25 # percentage: foreign words / words in the string

#TODO: decide what to do with single quotes, since they sometimes appear as part of a word
# fixes punctuation spacing for moses
# removes pipes
# lowercases
punct = re.compile(u'([.]|,|\?|!|:|;|\'|"|“|”|‘|’|—|\)|\()') #TODO: might need expanding
pipes = re.compile('\|') #finds pipes
spaces = re.compile('\s+') #finds successive whitespace in order to replace it with a single space character

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
                        print _("Dictionary %s not found, skipping...") % f
                        continue
        if len(words)> 0 and pollution/len(words) < POLLUTION_THRESHOLD:
            return line
        else:
            return None
    return line

def segment_units(store,lang1,lang2):
    from translate.tools import posegment
    from translate.lang import factory
    sourcelang = factory.getlanguage(lang1)
    targetlang = factory.getlanguage(lang2)
    segmenter = posegment.segment(sourcelang, targetlang)
    return segmenter.convertstore(store)

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
        u.source = fix_for_moses(u.source)
    if u.target:
        u.target = fix_for_moses(u.target)

    return u

def fix_for_moses(ustr): #pretends that abbreviations don't exist
    if ustr:
        nstr = punct.sub(u' \g<1> ', ustr)
        mstr = pipes.sub(u' ', nstr)
        ostr = spaces.sub(' ', mstr)
        return ostr.strip().lower()
    return None

def write_units(corpusname, mono, lang1=u"", lang2=u"", enc='utf-8', units=[], outdir=None):
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

def convert_store(file, cleanup, filters, lang1, lang2):
    try:
        store = factory.getobject(file)
        if segment:
            store = segment_units(store,lang1,lang2)
        for u in store.units:
                fix_unit(u, cleanup, filters)
        return store
    except ValueError, e:
        print _("%s; Could not convert %s to factory.") % (e,file)

def clear_previous(outdir, lang1, lang2):
    file_lang1 = os.path.join(outdir,corpusname + u"." + lang1)
    file_lang2 = os.path.join(outdir,corpusname + u"." + lang2)
    try:
        print _("Clearing previous contents of %s") % file_lang1
        s = codecs.open(file_lang1, 'w', 'utf-8')
        s.close()
    except IOError:
        print _("No file %s to be cleared") % file_lang1
    try:
        print _("Clearing previous contents of %s") % file_lang2
        t = codecs.open(file_lang2, 'w', 'utf-8')
        t.close()
    except IOError:
        print _("No file %s to be removed cleared") % file_lang2

def create_option_parser():
    """Creates command-line option parser for when this script is used on the
        command-line. Run "corpus_collect.py -h" for help regarding options."""
    from optparse import OptionParser
    usage='Usage: %prog [<options>] <language code 1> [<language code 2>] [<bilingual files>]'
    parser = OptionParser(usage=usage)

    parser.add_option(
        '-c', '--cleaner',
        dest='cleaner',
        choices = ["cleaner","daccleaner","webcleaner"],
        help=_('Specify the module to be used for cleaning.'),
        default=None
    )
    parser.add_option(
        '-f', '--filenames',
        dest='filenames',
        help=('Specify a file containing a list of names of files to be converted.'),
        default=None
    )
    parser.add_option(
        '-l', '--lang-filter',
        dest='filters',
        nargs=4,
        help=('Specify dictionary codes of languages to filtered out. Exactly four codes must be given, use - for empty tags.'),
        default=None
    )
    parser.add_option(
        '-m', '--mono',
        dest='mono',
        action='store_true',
        help=('Indicate that input is monolingual: only one output file results.'),
        default=False
    )
    parser.add_option(
        '-n', '--corpus_name',
        dest='corpusname',
        help=_('Specify corpus name.'),
        default='corpus'
    )
    parser.add_option(
        '-o', '--output-dir',
        dest='outputdir',
        help=_('Output directory to use. Default: location of input file.'),
        default='output'
    )
    parser.add_option(
        '-s', '--segment',
        dest='segment',
        help=_('Option to perform posegment on po files.'),
        action='store_true',
        default=False
    )
    return parser

if __name__ == "__main__":
    parser = create_option_parser()
    options, args = parser.parse_args()

    corpusname = options.corpusname
    outdir = options.outputdir
    cleanerchoice = options.cleaner #change to accommodate changes to cleaners...
    filters = options.filters
    mono = options.mono
    filenames = options.filenames
    segment = options.segment


    if cleanerchoice:
        import cleaner
        import daccleaner
        import webcleaner

        cleaners = {
                "cleaner":cleaner.Cleaner(),
                "daccleaner":daccleaner.DACCleaner(),
                "webcleaner":webcleaner.WebCleaner()
               }
        cleaner = cleaners[cleanerchoice]
        cleanup = cleaner.cleanup
    else:
        cleanup = None

    # get language codes
    if mono:
        if len(args) >= 1:
            lang1 = args[0]
            lang2 = lang1
        else:
            print parser.print_usage()
        exit(1)
    else:
        if len(args) >= 2:
            lang1 = args[0]
            lang2 = args[1]
        else:
            print parser.print_usage()
            exit(1)

    # clear files to be written from existing content
    clear_previous(outdir, lang1, lang2)

    # get list of files
    files = []
      # If file names are given as a file
    if filenames:
        n = codecs.open(filenames,'r','utf-8')
        lines = n.readlines()
        for l in lines:
            files.append(l.rstrip())

      # If file names aren't given in a file, they must be given as paramaters,
      #  as a list of files and/or directories.
      # Directories are not searched recursively
    elif len(args) >= 2:
        for f in args[2:]:
            if os.path.exists(f):
                if os.path.isdir(f):
                    for fn in os.listdir(f):
                        if not os.path.isdir(fn):
                            files.append(os.path.join(f, fn))
                else:
                    files.append(f)
        if len(files) == 0:
            print 'No input files specified.'
            exit(1)

    else:
        print parser.print_usage()
        exit()

    # convert and write
    for file in files:
        store = convert_store(file, cleanup, filters, lang1, lang2)
        if store:
            write_units(corpusname, mono, lang1, lang2, 'utf-8', store.units, outdir)
