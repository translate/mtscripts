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

class Cleaner:

    def __init__(self):
        self.tuplist = []
    
    def set_tuplist(self, t):
        self.tuplist = t

    def cleanup(self, ustr):
        global tuplist
        for t in tuplist:
            if t[1] == 'sub':
                ustr = t[0].sub(t[2],ustr)
            elif t[1] == 'del':
                if t[0].match(ustr):
                    return None
        #must remove any empty units here
        return ustr
    
    tuplist = []