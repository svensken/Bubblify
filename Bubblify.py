#!/usr/bin/python

import json, string
from pyparsing import (indentedBlock, Regex, Suppress, Group, Optional,
                       OneOrMore, restOfLine, Forward, Literal,
                       ParserElement, Combine, StringEnd)
import sys
 
ParserElement.setDefaultWhitespaceChars(' \t')
 
#COLON = Suppress(Literal(':'))
#label = Suppress(Literal('-')) + Group(OneOrMore(Regex(r'\w+'))) + COLON
label = Group(OneOrMore(Regex(r'\S+')))
nonWhite = Regex(r'\S+')
value = Combine(nonWhite + restOfLine)
item = Forward()
indentStack = [1]
item << (label + Optional(value) +
         Optional(indentedBlock(item, indentStack, True)))
 
parser = OneOrMore(indentedBlock(item, indentStack, False)) + StringEnd()

simplest = '''
a a
aa aa
    b
        c
            d
x
    y
    z
'''

moderate = '''
a
  a1 a2
b
  b1
    b11
c
'''

listy = parser.parseString(simplest)

[[   [ ['a', 'a'] ], [ ['aa', 'aa'], [[ ['b'], [[['c']]] ]] ], [['x'], [[['y']], [['z']]]]   ]]

print listy



#json.dumps(listy)