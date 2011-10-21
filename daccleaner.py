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
import cleaner

class DACCleaner(cleaner.Cleaner):
    def __init__(self):
        self.tuplist.append((re.compile('[ \t]+'),'sub',' '))
        self.tuplist.append((re.compile('^(.*?)[\n\f\r]'),'sub','\g<1>'))
        self.tuplist.append((re.compile('^[a-zA-Z]+[a-z \t,.!?"\']+$'),'keep',))

    def cleanup(self, ustr):
        for t in self.tuplist:
            if t[1] == 'sub':
                ustr = t[0].sub(t[2],ustr)
            elif t[1] == 'keep':
                if t[0].match(ustr) and len(ustr) > 4:
                    print ustr, len(ustr)
                    return ustr
                else:
                    return None
        return None