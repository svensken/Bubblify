#!/usr/bin/python

import json, string

###
# http://pyparsing.wikispaces.com/share/view/13557997
from pyparsing_1_5_7 import (indentedBlock, Regex, Suppress, Group, Optional,
                       OneOrMore, restOfLine, Forward, Literal,
                       ParserElement, Combine, StringEnd, 
                       ParseResults)
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
###

single_top = '''
a
  a1
    a11
      a111?
      a112fdsafdsafdsaf
      a113
    a12
    a13
  a2
  a3
    a31
  a4'''
"""
project name
  first component
    concerns
      weight
      speed
    simliar projects
      Elvis Parsely
      Ring of Doom
    foregone resources
      Jerry's Flowers
      rigid.js
    
  second component
    b1

  third component
"""

def sizable(name_str):
  # use a meaningful paramater of source text to adjust size of bubble. 
  # either something as basic as a <size> flag, or as awesome as auto-
  # detected importance of element ()

  l = len(name_str)
  if l > 8:
    return 80
  else:
    return 10*len(name_str)

def get_flags(name_str):
  flags = []
  if name_str.endswith('?'): flags.append('question')
  if 'awesome' in name_str.lower(): flags.append('awesome')

  if flags:
    return ' '.join(flags)
  else:
    return None


def sink(element):
  """ dictify element
  element can be one of two forms:
  parent: [[ ['name'], [[ ['child1'], ['child2'] ]] ]]
          note: child can be another block element itself
  child:  [[ ['name'] ]] """

  print '<<<dropped into>>>: ', element

  name_str = ' '.join( element[0][0] )
  element_is_parent = ( len(element[0]) == 2 )

  if element_is_parent:
    return { 
              "name":name_str, 
              "children": [ sink([child]) for child in element[0][1] ], 
              "flags":get_flags(name_str) 
            }
  else:
    return { 
              "name":name_str, 
              "size":sizable(name_str), 
              "flags":get_flags(name_str) 
            }



listy = parser.parseString(single_top)

dicty = sink(listy[0])
print dicty

with open( "reconstructed.json", "w" ) as outfile:
  json.dump(dicty, outfile)


