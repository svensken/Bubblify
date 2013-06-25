#!/usr/bin/python

import json, string

from pyparsing import (indentedBlock, Regex, Suppress, Group, Optional,
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
[
[
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
]
]

simplest = '''
level a
  kid a1
  kid a2
'''
[
[
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
]
]

single_top = """
project name
  first component
    concerns
      weight
      speed
    simliar projects
      Elvis Parsely
      Ring of Doom
    foregone resources
      Jerry's Paintballs
      rigid.js
    
  second component
    b1

  third component
"""

# def sink(element):
#   print '<<<dropped into>>>: ', element

#   for block in element:
#     name = block[0]
#     name_str = ' '.join(name)

#     #print 'bubble: ', name

#     if len(block) == 2: # is parent
#       print 'block is parent: ', block
      
#       children = block[1]

#       #top_dict["name"] = ' '.join(name)

#       print '  ^ child block: ', children

#       lower_container = []
#       for child in children:

#         print 'child: ', child
#         childname_str = ' '.join(child[0])
#         if len(child) == 2: # is parent
#           lower_container.append( 
#                           { "name":childname_str, "children":sink([child]) } 
#                           )
#         else: # no children
#           lower_container.append( 
#                           { "name":childname_str, "size":30} 
#                           )
#         print 'lower container: ', lower_container
#         print

#       return lower_container

#     else:
#       name = block[0]
#       print 'detected child: ', block
#       return { "name":name_str, "size":30 }


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
    return { "name":name_str, "children": [ sink([child]) for child in element[0][1] ] }
  else:
    return { "name":name_str, "size":300 }
  
  # lower_container = []
  # for block in element:
  #   name = block[0]
  #   name_str = ' '.join(name)

  #   #print 'bubble: ', name

  #   if len(block) == 2: # is parent
  #     print 'block is parent: ', block
  #     lower_container.append(  
  #                     { "name":name_str, "children":sink([child]) } 
  #                     )

  #     children = block[1]

  #     print '  ^ child block: ', children

  #     for child in children:

  #       print 'child: ', child
  #       print 'lower container: ', lower_container

  #     return { "name":name_str, "children":[sink([child]) for child in children] }

  #   else:
  #     print 'detected child: ', block
  #     return { "name":name_str, "size":30 }


listy = parser.parseString(single_top)

dicty = sink(listy[0])
#top_dict = { "name":"etwas", "children":dicty }
print dicty

with open( "reconstructed.json", "w" ) as outfile:
  json.dump(dicty, outfile)


# for a in listy:
#   print '1',a
#   for b in a:
#     print '2',b
#     for c in b:
#       print '3',c
#       for d in c:
#         print '4',d
#         for e in d:
#           print '5',e
#           for f in e:
#             print '6',f

data = { 
          "name":"a", 
          "children":
            [
              {"name":"a1","size":42},
              {"name":"a2","size":420}
            ] 
        }
print 'DATA:', repr(data)

data_string = json.dumps(data)
print 'JSON:', data_string








#json.dumps(listy)