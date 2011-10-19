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

import re

tuplist = []
#tuplist.append((re.compile('^[^a-z]+$'), 'del', '')) # deletes everything that is all caps or noise
#tuplist.append((re.compile('^.*[a-z]+.*[A-Z]'), 'del', '')) #deletes lines with internal capital letters
#tuplist.append((re.compile('^[a-zA-Z][.]'), 'del', '')) #deletes lines consisting of eg. "a."

#tuplist.append((re.compile('^([(\s]{0,10}[0-9]+[-\s.)/]*)+(.*?)'), 'sub', '\g<2>')) #removes numbers at the start of lines
#tuplist.append((re.compile('(.*?)\s[(\s]{0,10}[a-zA-Z]*([0-9]+[-\s.!)/]*)+$'), 'sub', '\g<1>')) #removes numbers at the end of lines

tuplist.append((re.compile('[ \t]+'),'sub',' '))
tuplist.append((re.compile('^(.*?)[\n\f\r]'),'sub','\g<1>'))

tuplist.append((re.compile('^[a-zA-Z]+[a-z \t,.!?"\']+$'),'keep',))

#~ #tuplist.append((re.compile(),,))

def cleanup(ustr):
    global tuplist
    for t in tuplist:
        if t[1] == 'sub':
            ustr = t[0].sub(t[2],ustr)
        elif t[1] == 'keep':
            if t[0].match(ustr) and len(ustr) > 4:
                print ustr, len(ustr)
                return ustr
            else:
                return None
    #print ustr
    #~ for t in tuplist:
        #~ if t[1] == 'sub':
            #~ temp = t[0].sub(t[2],ustr)
            #~ ustr = temp
            #~ #print 'sub:', ustr
        #~ elif t[1] == 'del':
            #~ if t[0].match(ustr):
                #~ #print 'del:', ustr
                #~ return None
    #must remove any empty units here
    return None