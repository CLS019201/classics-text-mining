
import re, json
infoboxes = []
num_docs = 0
total_docs = 0
skipped_1000s = 0

ex = [ "San Fernando Rey de Espana"]
with open ("../results/example_out_500.xml","a", encoding='utf-8') as wf:
    with open("../WIKIPEDIA/wiki/allwiki.xml", encoding='utf-8') as f:
        box_s = ''
        in_itembox = False
        has_locs = False
        #in_textbox = False
        opens = 0
        closes = 0
        lines = 0
        line_buffer = 0
        for line in f:
            if "</text>" in line:
                in_itembox = False
                has_locs = False
                in_textbox = False
                total_docs += 1
                if(total_docs % 10000 == 0):
                    print("total docs read:" + str(total_docs))
                continue # error handling... make sure we dont grab two text boxes
            #### HANDLING INFO BOXES
            if (in_itembox == False):
                if ("{{Infobox"  in line or "{{ Infobox"  in line): #(and "settlement" in line):
                    lines = 0
                    if (ex[0] in line):
                        continue
                    line = re.sub("\<.*\>","",line)
                    attr = line.strip().split(" ")
                    if (len(attr) > 1):
                        attr = attr[1]
                    else:
                        attr = ""
                    box_s = '<infobox ' + 'class="' + attr +'">\n'
                    opens = 0
                    closes = 0
                    in_itembox = True
            #START COLLECTING
            if (in_itembox):
                line_buffer += 1
                lines+= 1
                if (lines > 500):
                    print("THERE MAY BE AN ERROR")
                    skipped_1000s += 1
                    lines = 0
                    in_itembox = False
                    has_locs = False
                    in_textbox = False
                    continue # error handling... make sure we dont grab two text boxes
                opens += line.count("{{")
                closes += line.count("}}")
                box_s += line
                
                #look for latd and longd in line
                locs_keys = ['latd', 'longd', 'longitude', 'latitude']
                if any(key in line for key in locs_key:
                    #print('found lat')
                    #print(line)
                    #input()
                    has_locs = True

                if (opens == closes):
                    opens = 0
                    closes = 0
                    if has_locs:
                        #print("appending")
                        #input()
                        #infoboxes.append(box_s + '</infobox>\n')
                        num_docs += 1
                        wf.write(box_s + "</infobox>\n")
                        if(num_docs % 2000 == 0):
                            print(num_docs)
                            #print("BOXcount: " + str(num_docs))
                    has_locs = False
                    in_itembox = False

        #for box in infoboxes:
        #   f.write(box)

print("resuts:")
print(skipped_1000s)
print (str(total_docs))
print (str(num_docs))