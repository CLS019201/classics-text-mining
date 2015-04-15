import re

### HELPER FUNCTIONS ### (code is ugly already, these help a little)

# a janky system to collect infbox attributes, 
#takes the first string after {{infobox attr <ignored...>
def infobox_get_attr(line):
    attr = line.strip().split(" ")
    if (len(attr) > 1 and attr[1] != "infobox"):    #avoids {{ infobox case
        attr = attr[1]
    else:
        attr = ""
    return attr

def print_debug_t(total_docs):
    if(total_docs % 10000 == 0):
        print("total docs read:" + str(total_docs))

def print_debug_collected(num_docs):
    if(num_docs % 2000 == 0):
        print("###### USEFUL BOXES FOUND: " + str(num_docs))

# returns true if line contains something that we do not want
def exit_condition(line):
    if "</text>" in line:
        return True
    else:
        return False

def has_good_info(line):
    if any(key in line for key in __USEFUL_FLAGS):
        return True
    else:
        return False

################################################################################

### RUN ####
num_infoboxes = 0
num_docs = 0
total_docs = 0
skipped_chunks = 0
__max_box_lines = 500 #maximum num of lines in infobox before we throw it out
__USEFUL_FLAGS = ['latd', 'longd', 'longitude', 'latitude', 'coord', 'CoorHeader'
                  'coor d', 'Geolinks', 'Mapit', '| loc', 'coor_pinpoint', 'coordinates_']
_wikidb = "../WIKIPEDIA/wiki/allwiki.xml"
_outfile = "../results/example_out_500.xml"

# CLEAN THE FILE FIRST
with open (_outfile,"w", encoding='utf-8') as f:
    f.write('')

# Run this "state" machine...
with open (_outfile,"a", encoding='utf-8') as wf:
    with open(_wikidb,"r", encoding='utf-8') as f:
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
            if exit_condition(line):        # 1) so we do not cross boxes
                if lines > __max_box_lines:      # 2) we read unusually large infobox => there is probably an error
                    skipped_chunks += 1
                # Reset States
                lines = 0
                opens = 0
                closes = 0
                in_itembox = False
                has_locs = False
                # States Reset
                total_docs += 1
                print_debug_t(total_docs)
                continue

            #### Looking for start of infobox
            if (in_itembox == False):
                if ("{{Infobox"  in line or "{{ Infobox"  in line): #(and "settlement" in line):
                    # Reset states except in_itembox
                    lines = 0
                    opens = 0
                    closes = 0
                    has_locs = False
                    # Reset States
                    in_itembox = True
                    line = re.sub("\<.*\>","", line.strip()) #strip whitespace and <tag>
                    attr = infobox_get_attr(line)
                    box_s = '<infobox ' + 'class="' + attr +'">\n'

            #### Found start of infobox
            if (in_itembox):
                lines += 1
                opens += line.count("{{")
                closes += line.count("}}")
                box_s += line
                #look for useful data in line
                if has_good_info(line):
                    has_locs = True
                if (opens == closes):
                    num_infoboxes += 1
                    if has_locs:
                        num_docs += 1
                        wf.write(box_s + "</infobox>\n")
                        print_debug_collected(num_docs)
                    # Reset States
                    opens = 0
                    closes = 0
                    lines = 0
                    has_locs = False
                    in_itembox = False
                    # States Reset

with open("grab_items_log.txt", 'w') as log_f:
    log = ""
    log += "RESULTS and DIAGNOSTICS"
    log += "\nTotal number of docs:             " + str(total_docs)
    log += "\nTotal number of Infoboxes:        " + str(num_infoboxes)
    log += "\nNumber of Infoboxes Collected:    " + str(num_docs)
    log += "\nMax infobox chunk/line size:      " + str(__max_box_lines)
    log += "\nSKIPPED CHUNKS:                   " + str(skipped_chunks)
    print(log)
    log_f.write(log)


