import sanitizer
import re, json
from bs4 import BeautifulSoup

__USEFUL_FLAGS = ['latd', 'longd', 'latm', 'longm', 'lats','longs', 'latNS',
                    'longEW', '| name', '|name', 'official_name',"settlement_type",
                    'date', 'infobox']
_INFILE = "../results/settlement.xml"
_OUTFILE = "../results/settlement_1.xml"

def main():
    """
    s = sanitizer.Sanitizer(__USEFUL_FLAGS)
    s.clean(_INFILE, _OUTFILE)
    """
    allData = []
    soup = BeautifulSoup(open(_OUTFILE, encoding='utf-8'))
    print("soup cooked")
    entries = soup.find_all('infobox')
    for entry in entries:
        allData.append(getLocs(entry.string))
    with open ("../json/settlements_raw.json", "w") as f:
        json.dump(allData, f,sort_keys=True, indent=2)

#string -> dictionary
# returns dictionary of location information...
def getLocs(string):
    keys = ['latd', 'longd', 'latm', 'longm', 'lats','longs', 'latNS',
                    'longEW', 'established_date', 'extinct_date']
    data = {}
    data["_TYPE"] = "_SETTLEMENT"
    for k in keys:
        if (key in line for key in keys): 
            data[k] = grabVal(k, string)
    return data
# string -> string
# returns the val of | <wikikey> = <val> |
def grabVal(wikiKey, string):
    regex = re.compile(wikiKey+"\s*=\s*([^\|\n]*)")
    val = regex.findall(string)
    if val:
        return val[0].strip()
    else:
        return ""

if __name__ == "__main__":
    main()