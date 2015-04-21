import json, operator, re, sys
from bs4 import BeautifulSoup

__INFOBOXES_XML = "../results/sanitize1.xml"
__TARGET_DIR = "../results/"

def main(argv):
    grabber = ClassGrab(__INFOBOXES_XML, __TARGET_DIR+argv+".xml", "infobox", argv)
    grabber.run()
    return

class ClassGrab:
    betweenTag  = False
    # string, string, string, string
    # takes infile, outfile, a tag, and a class attribute anc constructs Grabber
    def __init__(self, infile, outfile, tag, tagClass):
        self.infile     = infile
        self.outfile    = outfile
        self.tag        = tag
        self.tagClass   = tagClass
        return
    # <self>
    # writes everything of the same tag and writes to outfile
    def run(self):
        ### Clean outfile
        with open(self.outfile, "w", encoding='utf-8') as f:
            f.write('')
        ### Open outfile and db - not using with for cleanliness
        outfile = open(self.outfile, "a", encoding='utf-8')
        infile      = open(self.infile, "r", encoding="utf-8")
        xmlText = ""
        for line in infile:
            self.betweenTag = self.betweenTag or "<"+self.tag+' class = "'+self.tagClass+'">' in line

            if self.betweenTag:
                xmlText += line
                if "</"+self.tag+">" in line:
                    outfile.write(xmlText)
                    self.betweenTag = False
                    xmlText = ""
        outfile.__exit__(None, None, None)
        infile.__exit__(None, None, None)
        return

if __name__ == "__main__":
    main(sys.argv[1])
