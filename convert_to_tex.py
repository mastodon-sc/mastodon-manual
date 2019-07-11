#! /usr/bin/python

from optparse import OptionParser
import re

parser = OptionParser()
( options, args ) = parser.parse_args()

infilename = "bla.tex"
outfilename = None
if len( args ) > 0 :
  infilename = args[ 0 ]
if len( args ) > 1 :
  outfilename = args[ 1 ]

f = open( infilename, 'r' )
text = f.read()
f.close()



# <wiki>text</wiki> is put into the wiki only
text = re.sub( r"<wiki>\n?(.*?)</wiki>\n?", r"", text, flags = re.DOTALL)


# <latex>text</latex> is put into the latex only
text = re.sub( r"<latex>\n?(.*?)</latex>\n?", r"\1", text, flags = re.DOTALL)


# dirty '#' handling in \wikilink
def escapepound(match):
  t = match.group(0)
  t = re.sub( r"#", r"\#", t )
  return t
text = re.sub( r"\\wikilink{(.*?)}", escapepound, text, flags = re.DOTALL)


if outfilename is None:
  print(text)
else:
  f = open( outfilename, 'w' )
  f.write( text )
  f.close()

