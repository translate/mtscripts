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

class WebCleaner(cleaner.Cleaner):
    
    def __init__(self):
        self.tuplist.append((re.compile('(.*?)\n(.+?)'), 'sub', '\g<1> \g<2>')) #removes newlines
        self.tuplist.append((re.compile('\[ URL.*'), 'del', ''))
        self.tuplist.append((re.compile('\[ COUNT.*'), 'del', ''))
        self.tuplist.append((re.compile('[\s]*Coat of Arms.*'), 'del', ''))
        self.tuplist.append((re.compile('Last Modified.*'), 'del', ''))
        self.tuplist.append((re.compile('Issued by.*'), 'del', ''))
        self.tuplist.append((re.compile('This site is best viewed.*'), 'del', ''))
        self.tuplist.append((re.compile('Developed and maintained.*'), 'del', ''))
        self.tuplist.append((re.compile('^www.services.gov.za.*'), 'del', ''))
        self.tuplist.append((re.compile('^About.*'), 'del', ''))
        self.tuplist.append((re.compile('\|\s*$'), 'sub', '')) #removes pipes at the end of a line
        self.tuplist.append((re.compile('\|'), 'sub', '\n'))   #replaces other pipes with newlines -- hack of sorts
        self.tuplist.append((re.compile('>>'), 'sub', '\n'))
        self.tuplist.append((re.compile('^\s*\[.*\]\s*$'), 'del', '')) #marks units starting and ending with square brackets
        self.tuplist.append((re.compile('\[.*?\]'), 'sub', '')) #removes anything between square brackets
        self.tuplist.append((re.compile('^\s*[0-9]+[.) ]*'), 'sub','')) #removes numbers at beginning of line
        self.tuplist.append((re.compile('[(]\s*[0-9]+(,\s*[0-9]+)*\s*[)]'),'sub','')) #removes comma seperated numbers in round brackets
        self.tuplist.append((re.compile('--|--'),'sub',' '))
        self.tuplist.append((re.compile('^\s*[\*.,?!:;]*\s*'),'sub',''))
        self.tuplist.append((re.compile('([A-Z][A-Za-z]+)\s[0-9]+(:\s*[0-9]+(-[0-9]+)*(,\s*[0-9]+(-[0-9]+)*)*)*'),'bib','')) #hopefully matches biblenames
        self.tuplist.append((re.compile('^[^A-Za-z]*$'),'del',''))
        self.tuplist.append((re.compile('[(]([^)]*$)'),'sub','\g<1>')) #removes unmatched (
        self.tuplist.append((re.compile('^([^(]*)[)]'),'sub','\g<1>')) #removes unmatched )
        self.tuplist.append((re.compile('^([A-Z]+\s){1,3}[A-Z]+$'),'del','')) #removes lines of all caps with up to four words
        self.tuplist.append((re.compile('^([a-z]*[A-Z]+[a-z]*\s){1,3}[a-z]*[A-Z]+[a-z]*$'),'del','')) #removes name-like lines
        #tuplist.append((re.compile(),,))

    def cleanup(self, ustr):
        for t in self.tuplist:
            if t[1] == 'sub':
                ustr = t[0].sub(t[2],ustr)
            elif t[1] == 'del':
                if t[0].match(ustr):
                    return None
            elif t[1] == 'bib':
                name = t[0].search(ustr)
                if name:
                    if self.isbiblename(name.group()):
                        ustr = t[0].sub(t[2],ustr)
        #must remove any empty units here
        return ustr
    
    def isbiblename(self, ustr):
        for b in self.biblenames:
            if ustr.lower().find(b) >= 0:
                return True
        return False
    
    biblenames = [
    "genesis","genesise","eksodus","eksodusi","levitikus","levitikusi","numeri","duteronomi",
    "yoshuwa","joshuwa","abagwebi","abahluleli","rute","ruthe","samuweli","amakhosi","kumkani",
    "kronike","ezra","nehemiya","estere","esteri","yobhi","jobe","indumiso","amahubo",
    "imizekeliso","izaga","intshumayeli","umshumayeli","ingoma yazo iingoma","isihlabelelo sezihlabelelo",
    "isaya","yeremiya","jeremiya","izililo","isililo","hezekile","hezekeli","daniyeli","hoseya",
    "yoweli","joweli","amosi","amose","obhadiya","obadiya","yona","jona","mika","nahum","nahume",
    "habhakuki","habakuki","zefaniya","hagayi","zekariya","malaki",
    "mateyu","mathewu","marko","marku","luka","yohane","johane","izenzo","roma","korinte",
    "galati","galathiya","efese","efesu","filipi","kolose","tesalonika","thesalonika",
    "timoti","thimothewu","tito","thithu","filemon","filemoni","hebhere","heberu",
    "yakobi","jakobe","petros","petru","yude","juda","isityhilelo","isambulo",
    "kol.", "eks.","tim.","thim."]