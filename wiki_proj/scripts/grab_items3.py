# grab_items3.py - making everything nice, an excercise in writing better python code,
# lets see what wrappin our code into classes does

import re

_USEFUL_FLAGS = [  'latd', 'longd', 'longitude', 'latitude', 'coord', 
                    'CoorHeader', 'coor d', 'Geolinks', 'Mapit', '| loc', 
                    'coor_pinpoint', 'coordinates_']

_WIKIDB = "../xml_data/allwiki.xml"
_OUTFILE = "../results/all_infoboxes.xml"
_LOGFILE = "../results/all_infoboxes_log.txt"
_MAX_BOX_SIZE = 500

def main():
    parser = Parser(_WIKIDB, _OUTFILE, _USEFUL_FLAGS, _MAX_BOX_SIZE)
    parser.resetStates()
    print(parser.db)
    parser.run()
    parser.writeLogs(_LOGFILE)

### PARSER CLASS
class Parser:

    # States
    unmatchedBraces = 0
    infoboxLines    = 0
    inInfobox       = False
    hasFlags        = False

    # Stats for logging
    totalDocs       = 0
    totalBoxes      = 0
    collectedBoxes  = 0
    skippedChunks   = 0

    # <self>, string, string, list
    # Constructor: takes two filepaths, and a list of strings of flags we want
    # to look for, and max infobox size for error handling
    def __init__(self, db, outfile, flags, maxBoxSize):
        self.db         = db
        self.outfile    = outfile
        self.flags      = flags
        self.maxBoxSize = maxBoxSize
        return

    # <self>
    # resets all states to 0 and false
    def resetStates(self):
        self.unmatchedBraces = 0
        self.infoboxLines    = 0
        self.inInfobox       = False
        self.hasFlags        = False
        return

    # <self>
    # resets all states, updates stats/log data, prints num total docs
    def resetAndUpdateLogs(self):
        self.resetStates()
        self.totalDocs += 1
        self.printTotalDocs()
        return
    # string -> string
    # returns <attr> from the string "{{infbox <attr> | <restofline>"
    def getInfoboxClass(self,line):
        attr = line.split("|")
        attr = re.sub("{{\s*Infobox","", attr[0])
        return attr.strip()


    ##############################################################
    #     Heart of the parser, this grabs all the Infoboxes      #
    ##############################################################

    # <self>
    # strips useful infoboxes from db and writes them to outfile
    # some rules:
    #   - states always rest before states are reset
    def run(self):
        ### Clean outfile
        with open(self.outfile, "w", encoding='utf-8') as f:
            f.write('')
        ### Open outfile and db - not using with for cleanliness
        outfile = open(self.outfile, "a", encoding='utf-8')
        db      = open(self.db, "r", encoding="utf-8")
        boxString = ""
        ### Run parser
        for line in db:
            # Exit conditions - errors in the markup
            if "</text>" in line:
                self.resetAndUpdateLogs()
                continue
            if self.infoboxLines > self.maxBoxSize:
                self.skippedChunks += 1
                self.resetAndUpdateLogs()
                continue

            # Loof for opening of infobox {{infobox
            if not self.inInfobox:
                if ("{{Infobox"  in line or "{{ Infobox"  in line):
                    self.inInfobox = True
                    line = re.sub("\<.*\>","", line.strip()) #remove tags, spaces
                    attr = self.getInfoboxClass(line)
                    boxString = '<infobox class = "' + attr + '">\n'
            # in infobox, lets check the strings
            if self.inInfobox:
                self.infoboxLines += 1
                self.unmatchedBraces += line.count("{{") - line.count("}}")
                boxString += line.strip() + "\n"
                self.hasFlags = self.hasFlags or any(key in line for key in self.flags)
                if self.unmatchedBraces == 0:
                    self.totalBoxes += 1
                    if self.hasFlags:
                        self.collectedBoxes += 1
                        outfile.write(boxString + "</infobox>\n")
                        self.printCollected() # write this func TODO
                    self.resetStates()

        ### Exit Files
        outfile.__exit__(None, None, None)
        db.__exit__(None, None, None)
        return

    ########################################################################

    #### Other funcs

    def printTotalDocs(self):
        interval = 10000
        if self.totalDocs >= interval and self.totalDocs % interval == 0:
            print("Total docs read: " +str(self.totalDocs))
    def printCollected(self):
        interval = 5000
        if self.collectedBoxes >= interval and self.collectedBoxes % interval == 0:
            print("Total docs read: " +str(self.collectedBoxes))

    # <self>
    # prints and write logs to logfile
    def writeLogs(self, logfile):
        with open(logfile, 'w') as log_f:
            log = ""
            log += "RESULTS and DIAGNOSTICS"
            log += "\nTotal number of docs:             " + str(self.totalDocs)
            log += "\nTotal number of Infoboxes:        " + str(self.totalBoxes)
            log += "\nNumber of Infoboxes Collected:    " + str(self.collectedBoxes)
            log += "\nMax infobox chunk/line size:      " + str(self.maxBoxSize)
            log += "\nSKIPPED CHUNKS:                   " + str(self.skippedChunks)
            print(log)
            log_f.write(log)

#### END OF CLASS

if __name__ == "__main__":
    main()