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

bricks = '''
a
b
  b1
    b11
      b111
  b2
c
d
  d1
'''
[[
[
  ['a']
], 
[
  ['b'], 
    [
      [
        ['b1'], 
          [
            [
              ['b11'],
                [
                  [
                    ['b111']
                  ]
                ]
            ]
          ]
      ], 
      [
        ['b2']
      ]
    ]
], 
[
  ['c']
], 
[
  ['d'], 
    [
      [
        ['d1']
      ]
    ]
]
]]

moderate = '''
a
  a1 a2
b
  b1
    b11
c
'''

[[   
\
[ 
  ['a', 'a'] 
] , 
\
[ 
  ['aa', 'aa']        , 
[ [ ['b']             , 
[ [   ['c'] ]] ]]
] ,
\
[ ['x']               , 
[ [ ['y'] ]           , 
  [ ['z'] ]] 
      ]   
\
]]
simplest = '''
a
  a1
  a2
'''
[[
[ 
  ['a'], 
    [
      [
        ['a1']
      ], 
      [
        ['a2']
      ]
    ]
]
]]

listy = parser.parseString(simplest)
print listy

for l in listy[0]:
  print l

data = { "name":"a", "children":[{"name":"a1","size":42},{"name":"a2","size":420}] }
print 'DATA:', repr(data)

data_string = json.dumps(data)
print 'JSON:', data_string








#json.dumps(listy)