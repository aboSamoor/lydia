import xml.sax
from xml.sax.saxutils import escape

class subTree(xml.sax.ContentHandler):
    def __init__(self, tag, op=None):
        self.tag = tag
        self.inside = False
        self.text = ""
        self.counter = 0
        if op:
            self.operation = op
        else:
            self.operation = self.dummy_op

    def startElement(self, name, attrs):
        self.last_opentag = name  # think about <id><id></id></id>
        if name == self.tag:
            self.inside = True 
        if self.inside:
            self.text += "<"+name
            if attrs.keys():
                self.text += ' '
            for i,j in attrs.items():
                self.text += i + '='+'"'+j+'"'
            self.text += '>'
            self.counter = len(self.text)
        else:
            self.text = ""

    def endElement(self, name):
        if self.inside:
            if len(self.text) > self.counter: # something has been added
                self.text = self.text[:self.counter] + escape(self.text[self.counter:])
            self.text += "</"+name+">"
            self.counter = len(self.text)
        else:
            self.text = ""
        if name == self.tag:
            self.operation(self.text)
            self.inside = False
            self.text = ""

    def dummy_op(self, text):
        pass
    
    def characters(self, content):
        self.text += content
    
def rmExTags(text):
    start = text.find('>')
    end = text.rfind('<')
    return text[start+1:end]
