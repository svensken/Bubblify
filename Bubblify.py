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

listy = parser.parseString(simplest)
print type(listy)
print isinstance(listy, ParseResults)

top_dict = {}
lower_dict = {}

# def ssink(element):
#   print 'ELEMENT: ', element
#   for block in element:

#     block_is_parent = ( len(block) == 2 )

#     if block_is_parent:
#       name = block[0]
#       children = block[1]

#       top_dict["name"] = ' '.join(name)

#       print 'parent: ', name
#       print 'child block: ', children

#       for child in children:
#         print 'child: ', ' '.join( child[0] )
#         sink([child])
#         lower_dict["name"] = ' '.join( child[0] )
#         lower_dict["size"] = 300
#         lower_container.append(lower_dict)
#         print lower_container
#       top_dict["children"] = [d for d in lower_container]
#       print 'top_dict: ',top_dict

#     else:
#       print 'non parent: ', block
#       #name = block[0]
#       #top_dict["name"] = ' '.join(name) 

#   return top_dict

def sink(element):
  print '<<<dropped into>>>: ', element

  for block in element:
    name = block[0]
    name_str = ' '.join(name)

    #print 'bubble: ', name

    if len(block) == 2: # is parent
      print 'block is parent: ', block
      
      children = block[1]

      #top_dict["name"] = ' '.join(name)

      print '  ^ child block: ', children

      lower_container = []
      for child in children:

        print 'child: ', child
        childname_str = ' '.join(child[0])
        if len(child) == 2: # is parent
          lower_container.append( 
                          { "name":childname_str, "children":sink([child]) } 
                          )
        else: # no children
          lower_container.append( 
                          { "name":childname_str, "size":300} 
                          )
        print 'lower container: ', lower_container
        print

      return lower_container

    else:
      name = block[0]
      print 'detected child: ', block
      return { "name":name_str, "size":300 }



dicty = sink(listy[0])
top_dict = { "name":"etwas", "children":dicty }

def dictify(element):
  print element
  dicty["name"] = element[0][0]
  dicty["children"] = element[1][0]
  print dicty
  # for piece in element:
  #   print piece
  # if type(element)==list:
  #   return element[0]
  # elif type(element)==str:
  #   print element

#sink( listy[0][0] )

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