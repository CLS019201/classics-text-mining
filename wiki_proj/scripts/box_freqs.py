import json, operator, re

def get_class(line):
    line = line[16:]
    line = re.sub('"',"", line)
    line = re.sub(">","",line)
    line = re.sub('\r\n', "", line)
    return line

def main():
    #list 
    freq = {}
    with open ("../xml_data/sanitize_1.xml","r", encoding="utf-8") as f:
        for line in f:
            if "<infobox" in line:
                line = get_class(line)
                if line in freq:
                    freq[line] += 1
                else:
                    freq[line] = 1
    # list tuples
    pairs = []
    for attr in freq:
        if freq[attr] > 80:
            pairs.append((attr, freq[attr]))

    ordered_list = sorted(pairs, key = lambda tup:tup[1], reverse=True)

    with open ("../json/list_attr.json", "w") as f:
        json.dump(ordered_list, f, indent=2)

if __name__ == "__main__":
    main()