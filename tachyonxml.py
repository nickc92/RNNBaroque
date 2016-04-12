from xml.dom import minidom

class XMLNode:
    theElem = None
    
    def __init__(self, inElem):
        self.theElem = inElem
        self.name = self.theElem.nodeName

    def getChildNodes(self, name):
        nodes = self.theElem.getElementsByTagName(name)
        retNodes = []
        for i in range(nodes.length):
            retNodes.append(XMLNode(nodes.item(i)))
            
        return retNodes

    def getChildNode(self, name):
        nodes = self.theElem.getElementsByTagName(name)
        if nodes.length == 0: return None
        if nodes.length > 1: raise Exception, 'More than one child node named ' + name
        return XMLNode(nodes.item(0))

    def getIntAttr(self, name): return int(self.theElem.getAttribute(name))

    def getFloatAttr(self, name): return float(self.theElem.getAttribute(name))

    def getAttr(self, name): return str(self.theElem.getAttribute(name))

    def __getitem__(self, name): return self.getAttr(name)
        
    def hasAttr(self, name): return self.theElem.hasAttribute(name)

    def getValue(self): return self.theElem.firstChild.data

    def __str__(self): return self.theElem.toprettyxml(newl='')
        

def XMLParseFile(fl):
    return XMLNode(minidom.parse(fl))

def XMLParseString(st):
    return XMLNode(minidom.parseString(st))

    

    
