import json,re
has_dates = 0
total = 0
has_locs = 0
def main():
    clean_data = []
    with open("../json/settlements_raw.json","r", encoding="utf-8") as f:
        raw_data = json.load(f)
        for entry in raw_data:
            new = normalize(entry)
            if new['lat'] != 0 and new['lng'] != 0:
                global has_locs
                has_locs += 1
                clean_data.append(new)
    with open ("../json/settlements_locs.json", "w", encoding="utf-8") as f:
        json.dump(clean_data, f,sort_keys=True, indent=2)
    print("HAS DATES")
    print(has_dates)
    print("TOTAL")
    print(total)
    print("has_locs")
    print(has_locs)

def normalize(entry):
    entry = cleanComments(entry)
    if entry['established_date'] != "":
        global has_dates
        has_dates += 1
    global total
    total += 1
    data = {"_TYPE": "_SETTLEMENT",
            "established_date": entry["established_date"],
            "extinct_date": entry["extinct_date"]
            }
    # handle lat
    lat = 0
    lng = 0
    try:
        if entry['latd'] != "":
            lat += float(entry['latd'])
    except:
        pass
    try:
        if entry['latm'] != "":
            lat += float(entry['latm']) / 60
    except:
        pass
    try:
        if entry['lats'] != "":
            lat += float(entry['lats']) / 3600
    except:
        pass
    try:
        if entry['latNS'] != "":
            if "S" in  entry['latNS']:
                lat = lat * -1
    except:
        pass
    try:
        # handle lng
        if entry['longd'] != "":
            lng += float(entry['longd'])
    except:
        pass
    try:
        if entry['longm'] != "":
            lng += float(entry['longm']) / 60
    except:
        pass
    try:
        if entry['lats'] != "":
            lng += float(entry['longs']) / 3600
    except:
        pass
    try:
        if entry['longEW'] != "":
            if "W" in  entry['longEW']:
                lng = lng * -1
    except:
        pass
    ###
    data["lat"] = lat
    data['lng'] = lng
    return data

def cleanComments(entry):
    for k in entry:
        entry[k] = re.sub("<.*>","",entry[k])
    return entry

if __name__ == "__main__":
    main()

