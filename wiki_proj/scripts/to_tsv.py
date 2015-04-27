# Converts our current JSON to GeoJSON in preparation for D3 map viz

import json, copy, re

def getDate(date):
    date = str(date)
    if "century" in date:
        if ("B" not in date and "C" not in date) or ("b" not in date and "c" not in date):
            digits = ''.join(c for c in date if c.isdigit())
            if digits:
                return str(int(digits) + 1 * 1000)
        else:
            return "BAD"
    else:
        regex = re.compile("(\d\d\d\d)")
        val = regex.findall(date)
        if val: 
            return str(val[0])
    return "BAD"


def round_down(num, divisor):
    return num - num%divisor


def main():
    with open("../viz/json/dated_americas.tsv", "a") as a:
        a.write("")
    with open("../viz/json/dated_americas.tsv", "a") as a:
        a.write("0\t1\tdate\n")
        garbage = 0
        good = 0
        year_freq = {}
        with open("../json/dated_settlements_locs.json","r") as f:
            raw_data = json.load(f)
            for entry in raw_data:
                date = getDate(entry["established_date"])
                if "BAD" not in date and int(date) <= 2015:
                    with open("dates.txt", "a", encoding="utf-8") as d:
                        d.write(str(date) + "\n")

                    rounded = round_down(int(date), 10)
                    if rounded in year_freq:
                        year_freq[rounded] += 1
                    else:
                        year_freq[rounded] = 1

                    

                    a.write(str(entry["lng"]) + "\t" + str(entry["lat"]) + "\t" + "01/01/"+ date + "\n")
                    good += 1
                else:
                    garbage += 1
        print(good)
        print(garbage)
        with open("buckets.json", "w") as d:
            json.dump(year_freq, d, sort_keys=True, indent=2)



if __name__ == "__main__":
    main()
