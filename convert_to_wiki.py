#! /usr/bin/python

from optparse import OptionParser
import re

parser = OptionParser()
( options, args ) = parser.parse_args()

infilename = "wiki.wtex"
outfilename = None
if len( args ) > 0 :
  infilename = args[ 0 ]
if len( args ) > 1 :
  outfilename = args[ 1 ]

f = open( infilename, 'r' )
text = f.read()
f.close()



# <wiki>text</wiki> is put into the wiki only
text = re.sub( r"<wiki>\n?(.*?)</wiki>\n?", r"\1", text, flags = re.DOTALL)


# <latex>text</latex> is put into the latex only
text = re.sub( r"<latex>\n?(.*?)</latex>\n?", r"", text, flags = re.DOTALL)





# \section{x} to == x == etc.
text = re.sub( r"\\section{(.*?)}", r"== \1 ==", text, flags = re.DOTALL)
text = re.sub( r"\\subsection{(.*?)}", r"=== \1 ===", text, flags = re.DOTALL)
text = re.sub( r"\\subsubsection{(.*?)}", r"==== \1 ====", text, flags = re.DOTALL)


# itemize
def itemize(match):
  return re.sub( r"^\s*\\item", "*", match.group(1), flags = re.MULTILINE)
text = re.sub( r"\\begin{itemize}(.*?)\\end{itemize}", itemize, text, flags = re.DOTALL)


# remove verbatim
def verbatim(match):
  return "\n" + re.sub( r"^", " ", match.group(1), flags = re.MULTILINE) + "\n"
text = re.sub( r"\\begin{Verbatim}\n(.*?)\n\\end{Verbatim}", verbatim, text, flags = re.DOTALL)


# remove %comments
text = re.sub( r"^%(.*?)\n", r"", text, flags = re.DOTALL | re.MULTILINE)
text = re.sub( r"([^\\])%(.*?)\n", r"\1\n", text, flags = re.DOTALL)


# ``...'' to "..."
text = re.sub( r"``(.*?)''", r'"\1"', text, flags = re.DOTALL)


# \emph{x} to ''x''
text = re.sub( r"\\emph{(.*?)}", r"''\1''", text, flags = re.DOTALL)


# $x$ to ''x''
text = re.sub( r"\$([^$\n]*?)\$", r"''\1''", text, flags = re.DOTALL)


# \texttt{x} to <tt>x</tt>
text = re.sub( r"\\texttt{(.*?)}", r'<tt style="font-size: 1.25em;">\1</tt>', text, flags = re.DOTALL)


# \dots to ...
text = re.sub( r"\\dots", r"...", text, flags = re.DOTALL)


# \times to &times;
text = re.sub( r"\\times\s", r"&times;", text, flags = re.DOTALL)


# remove \\
text = re.sub( r"\\\\", r"", text, flags = re.DOTALL)


# remove \noindent
text = re.sub( r"\\noindent\n?", r"", text, flags = re.DOTALL)


# \wikilink{...}{...} to [[...|'''...''']]
text = re.sub( r"\\wikilink{(.*?)}{(.*?)}", r"[[\1|'''\2''']]", text, flags = re.DOTALL)


# \keys{...} to {{key press|...}}
def keys(match):
  t = match.group(1);
  t = re.sub( r"\\cmd", r"Cmd", t );
  t = re.sub( r"\\ctrl", r"Ctrl", t );
  t = re.sub( r"\\shift", r"Shift", t );
  t = re.sub( r"\\arrowkeyup", r"Up", t );
  t = re.sub( r"\\arrowkeydown", r"Down", t );
  t = re.sub( r"\\arrowkeyleft", r"Left", t );
  t = re.sub( r"\\arrowkeyright", r"Right", t );
  t = re.sub( r"\s*\+\s*", r"|", t );
  t = re.sub( r"LATEXGROUPEDPLUS", r"+", t );
  return r"KEYPRESSOPENkey press|" + t + "KEYPRESSCLOSE"
text = re.sub( r"{\+}", r"LATEXGROUPEDPLUS", text, flags = re.DOTALL)
text = re.sub( r"\\keys{(.*?)}", keys, text, flags = re.DOTALL)
text = re.sub( r"LATEXGROUPEDPLUS", r"{+}", text, flags = re.DOTALL)


# \menu{x} to {{bc | ...}}
def menu(match):
  t = match.group(1);
  t = re.sub( r"\s*\>\s*", r" | ", t );
  return r"KEYPRESSOPENbc | " + t + "KEYPRESSCLOSE"
text = re.sub( r"\\menu{(.*?)}", menu, text, flags = re.DOTALL)


# \button{x} to ''x''
text = re.sub( r"\\button{(.*?)}", r"''\1''", text, flags = re.DOTALL)


# \& to &
text = re.sub( r"\\&", r"&", text, flags = re.DOTALL)


# \% to %
text = re.sub( r"\\%", r"%", text, flags = re.DOTALL)





# tables
text = re.sub( r"^\s*\\tablecell(\[.*?\])?{(.*?)}", r'| style="padding: 5px;" | \2', text, flags = re.DOTALL | re.MULTILINE)
text = re.sub( r"\\specialcell{(.*?)}", r"\1", text, flags = re.DOTALL)
text = re.sub( r"^\s*\\hline", r"|-", text, flags = re.DOTALL | re.MULTILINE)



# latex macros
text = re.sub( r"\\ie", r"i.e.", text, flags = re.DOTALL)
text = re.sub( r"\\eg", r"e.g.", text, flags = re.DOTALL)
text = re.sub( r"\\Ie", r"I.e.", text, flags = re.DOTALL)
text = re.sub( r"\\Eg", r"E.g.", text, flags = re.DOTALL)
text = re.sub( r"\\etc", r"etc", text, flags = re.DOTALL)
text = re.sub( r"\\bdv", r"BigDataViewer", text, flags = re.DOTALL)
text = re.sub( r"\\Bdv", r"BigDataViewer", text, flags = re.DOTALL)
text = re.sub( r"\\bds", r"BigDataServer", text, flags = re.DOTALL)
text = re.sub( r"\\Bds", r"BigDataServer", text, flags = re.DOTALL)
text = re.sub( r"\\screenshotA{(.*?)}", r"[[Image:bdv-\1]]", text, flags = re.DOTALL)
text = re.sub( r"\\screenshotB{(.*?)}", r"[[Image:bdv-\1|500px]]", text, flags = re.DOTALL)
text = re.sub( r"\\screenshotTikz{(.*?)}", r"[[Image:bdvTikz-\1.png]]", text, flags = re.DOTALL)


# clean up
text = re.sub( r"KEYPRESSOPEN(.*?)KEYPRESSCLOSE", r"{{\1}}", text, flags = re.DOTALL)

if outfilename is None:
  print text
else:
  f = open( outfilename, 'w' )
  f.write( text )
  f.close()

