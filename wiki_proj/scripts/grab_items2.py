import re

##### GLOBALS #####

__USEFUL_FLAGS = ['latd', 'longd', 'longitude', 'latitude', 'coord', 'CoorHeader'
                  'coor d', 'Geolinks', 'Mapit', '| loc', 'coor_pinpoint', 'coordinates_']
_wikidb = "../examples_latd+infobox.xml"
_outfile = "../testout.xml"

# Setting logging variables to collect stats
totalBoxes = 0
collectedBoxes = 0
totalDocs = 0
skippedChunks = 0
__max_box_lines = 500 #maximum num of lines in infobox before we throw it out

def main():
    # CLEAN THE FILE FIRST
    with open (_outfile,"w", encoding='utf-8') as f:
        f.write('')
    collectInfoboxes(_wikidb,_outfile,"../testlogs.txt")
    
    #writeLogs("../testlogs.txt")

def collectInfoboxes(wikifile, outfile,logfile):
    totalBoxes = 0
    collectedBoxes = 0
    totalDocs = 0
    skippedChunks = 0
    __max_box_lines = 500 #maximum num of lines in infobox before we throw it out
    with open (outfile,"a", encoding='utf-8') as wf:
        with open(wikifile,"r", encoding='utf-8') as f:
            box_s = ''
            # Reset States
            opens = 0
            closes = 0
            lines = 0
            in_itembox = False
            has_locs = False
            # Reset States
            for line in f:
                #### Check EXIT CONDITIONS 1st
                if "</text>" in line:        # 1) so we do not cross boxes
                    if lines > __max_box_lines:      # 2) we read unusually large infobox => there is probably an error
                        skippedChunks += 1
                    # Reset States
                    lines = 0
                    opens = 0
                    closes = 0
                    in_itembox = False
                    has_locs = False
                    # States Reset
                    totalDocs += 1
                    printTotalDocs()
                    continue

                #### Looking for start of infobox
                if in_itembox == False:
                    if ("{{Infobox"  in line or "{{ Infobox"  in line): #(and "settlement" in line):
                        # Reset states except in_itembox
                        lines = 0
                        opens = 0
                        closes = 0
                        has_locs = False
                        # Reset States
                        in_itembox = True
                        line = re.sub("\<.*\>","", line.strip()) #strip whitespace and <tag>
                        attr = getItemBoxClass(line)
                        box_s = '<infobox ' + 'class="' + attr +'">\n'

                #### Found start of infobox
                if in_itembox:
                    lines += 1
                    opens += line.count("{{")
                    closes += line.count("}}")
                    box_s += line
                    #look for useful data in line
                    if any(key in line for key in __USEFUL_FLAGS):
                        has_locs = True
                    if opens == closes:
                        totalBoxes += 1
                        if has_locs:
                            collectedBoxes += 1
                            wf.write(box_s + "</infobox>\n")
                            printCollected()
                        # Reset States
                        opens = 0
                        closes = 0
                        lines = 0
                        has_locs = False
                        in_itembox = False
                        # States Reset

        with open(logfile, 'w') as log_f:
            log = ""
            log += "RESULTS and DIAGNOSTICS"
            log += "\nTotal number of docs:             " + str(total_docs)
            log += "\nTotal number of Infoboxes:        " + str(totalBoxes)
            log += "\nNumber of Infoboxes Collected:    " + str(collectedBoxes)
            log += "\nMax infobox chunk/line size:      " + str(__max_box_lines)
            log += "\nSKIPPED CHUNKS:                   " + str(skippedChunks)
            print(log)
            log_f.write(log)

### HELPER FUNCTIONS ### (code is ugly already, these help a little)

# string -> string
# returns string of infobox type  {{infobox <attr> |
def getItemBoxClass(line):
    attr = line.strip().split(" ")
    if (len(attr) > 1 and attr[1] != "infobox"):    #avoids {{ infobox case
        attr = attr[1]
    else:
        attr = ""
    return attr

# int -> print
# prints number of documents read for every 10,000 docs
def printTotalDocs():
    if(totalDocs % 10000 == 0):
        print("total docs read:" + str(totalDocs))

# int -> print
# prints number of itemboxes colected for every 2000 boxes
def printCollected():
    if(collectedBoxes % 2000 == 0):
        print("###### USEFUL BOXES FOUND: " + str(collectedBoxes))

main()