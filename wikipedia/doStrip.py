#!/usr/bin/env python

import re
import sys

reObjs = []
reSubWith = []

# 0: Titles
Titles = re.compile("^(?P<equals>[=]{2,5})[ ]*([^\n]*)[ ]*(?P=equals)(?=(.*?)\n)", re.M)
 
reObjs.append(Titles) 	
reSubWith.append("\\2")

# 1: Comments
Comments = re.compile("[~]{3,5}")
reObjs.append(Comments)
reSubWith.append("")

# 2: Bold and Italic
BoldItalic = re.compile("(?P<marks>'''''|'''|'')(.*?)(?P=marks)")
reObjs.append(BoldItalic)
reSubWith.append("\\2") 

# 3: Lists and Definitions
ListDef = re.compile("^[#*:;]+", re.M)
reObjs.append(ListDef)
reSubWith.append("")

# 4: Horizontal Lines
hLine = re.compile("^[-]{4,}", re.M)
reObjs.append(hLine)
reSubWith.append("")

# 5: External Links
exLink = re.compile("([[])?(?(1)|(^|(?<=[ \t\n\r])))(http://|https://|ftp://|irc://|gopher://|telnet://|nntp://|worldwind://|mailto:|news:)([^ \t\n\r]*)(?(1)[ ])?(.*?|\\B|\\b)(?(1)[]])", re.I)
reObjs.append(exLink)
reSubWith.append("\\5")

# 6: Reference Tag and References List (Iterate Till No Match)
Refs = re.compile("<(?P<tag>ref|references)([ ].*?)?(/)?>(?(3)|(.*?)</(?P=tag)>)", re.S | re.I)
reObjs.append(Refs)
reSubWith.append("")

# 7: Leading Spaces
lSpaces = re.compile('^[ ]+', re.M)
reObjs.append(lSpaces)
reSubWith.append("")

# 8: HTML Comments
HTMLComments = re.compile("<!--.*?-->", re.S)
reObjs.append(HTMLComments)
reSubWith.append("")

# 9: HTML Tags: code, math, var, ruby, rb, rt, rp, hr, br (Iterate Till No Match)
HTMLTags1 =re.compile("<(?P<tag>code|math|var|ruby|rb|rt|rp|hr|br)([ ].*?)?(/)?>(?(3)|(.*?)</(?P=tag)>)", re.I | re.S)
reObjs.append(HTMLTags1)
reSubWith.append("")

# 10: HTML Tags: b, big, blockquote, caption, center, cite, dd, div, dl, dt, em, font, h1, h2, h3, h4, h5, h6, i, li, ol, p, s, small, strike, strong, sub, sup, table, td, th, tr, tt, u, ul, nowiki, pre (Iterate Till No Match)
HTMLTags2 =re.compile("<(?P<tag>b|big|blockquote|caption|center|cite|dd|div|dl|dt|em|font|h1|h2|h3|h4|h5|h6|i|li|ol|p|s|small|strike|strong|sub|sup|table|td|th|tr|tt|u|ul|nowiki|pre)([ ].*?)?(/)?>((?(3)(\\b|\\B)|.*?))(?(3)|</(?P=tag)>)", re.I | re.S) 
reObjs.append(HTMLTags2)
reSubWith.append("\\4")

# 11: Tables and Templates
TablesTemplates = re.compile("{[{]?([^{]*?)[}]?}([\n]?)", re.S)
reObjs.append(TablesTemplates)
reSubWith.append("")

# 12: Internal Links (and others)
inLinks = re.compile("[[]{2}([^]|[]*)[|]?([^][]*?)[]]{2}", re.S)
reObjs.append(inLinks)
def internalLinkSub(matchObj):
	if matchObj.group(1).find(":") != -1:
		return ""
	if matchObj.group(2) != "":
		return matchObj.group(2)
	return matchObj.group(1).replace("#"," ").lstrip()
reSubWith.append(internalLinkSub)

# 13: HTML Coded Characters (Full List: http://www.w3.org/TR/html401/sgml/entities.html)
HTMLCodedChars = re.compile("&([^ ]*?);")
reObjs.append(HTMLCodedChars)
def codedChars(matchObj):
	entity = matchObj.group(1).lower()
	if entity == "nbsp":
		return " "
	if entity == "ndash":
		return "-"
	if entity == "mdash":
		return "-"
	if entity == "lt":
		return "<"
	if entity == "gt":
		return ">"
	if entity == "amp":
		return "&"
	if entity == "quot":
		return "\""
	if entity[0] == "#":
		if entity[1] == "x":
			return unichr(int(entity[2:], 16))
		return unichr(int(entity[1:]))
	return ""
reSubWith.append(codedChars)

#14 Extra new lines and spaces
ExtraNewLines = re.compile("\n[\n]+[\B]*[\n]*")
reObjs.append(ExtraNewLines)
reSubWith.append("\n")

#Extra Ref removal
ExtraRefs=re.compile(r'<ref ((.*?)=(.*?))*>(.*)</ref>')
reObjs.append(Refs)
reSubWith.append("")

def dewikify(x):
    y = x
    for i in range(0, len(reObjs)):
        while reObjs[i].search(y):
            y = reObjs[i].sub(reSubWith[i], y)
    return y


if __name__=="__main__":
    try:
        hi = open(sys.argv[1],"rb")
    except IOError:
        pass
    else:
        x = hi.read()
        try:
            x  = dewikify(x)
        except:
            pass
        else:
            ho = open(sys.argv[1]+".f","w")
            try:
                ho.write(x)
            except:
                pass
            ho.close()
    finally:
        hi.close()
