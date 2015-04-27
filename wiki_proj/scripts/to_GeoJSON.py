# Converts our current JSON to GeoJSON in preparation for D3 map viz

import json, copy

def main():
    new_data = {}
    new_data["type"] = "FeatureCollection"
    new_data["features"] = []
    # america = copy.deepcopy(new_data)
    # south_america = copy.deepcopy(new_data)
    americas = copy.deepcopy(new_data)

    with open("../viz/json/dated_americas.tsv", "a") as a:
        a.write("0\t1\tdate\n")
        # world = copy.deepcopy(new_data)
        with open("../json/dated_settlements_locs.json","r") as f:
            raw_data = json.load(f)
            stop = 0
            for entry in raw_data:
                feature = {"type":"", 
                           "geometry":{"coordinates":[]},
                           "properties":{"type":"", "est_date":"", "ext_date":""}
                           }
                feature["type"] = "Feature"
                feature["geometry"]["type"] = "Point"
                feature["geometry"]["coordinates"] = [entry["lng"], entry["lat"]]
                feature["properties"]["type"] = entry["_TYPE"]
                feature["properties"]["type"] = entry["_TYPE"]
                feature["properties"]["est_date"] = entry["established_date"]
                feature["properties"]["ext_date"] = entry["extinct_date"]
                # world["features"].append(feature)
                # if entry["lat"] >= 24 and entry["lat"] <= 50 and -125 <= entry["lng"] and entry["lng"] <= -66:
                #     america["features"].append(feature)
                # if entry["lat"] >= -57.0 and entry["lat"] <= 14.0 and -94.0 <=entry["lng"] and entry["lng"] <= -32.0:
                #     south_america["features"].append(feature)
                if entry["lat"] >= -60.0 and entry["lat"] <= 84.0 and -171 <=entry["lng"] and entry["lng"] <= -26.0:
                    americas["features"].append(feature)
                    a.write(str(entry["lng"]) + "\t" + str(entry["lat"]) + "\t" + "07/01/1962" + "\n")

                





    # with open ("../json/dated_america.json", "w") as f:
    #     json.dump(america, f)
    # with open ("../json/dated_south_america.json", "w") as f:
    #     json.dump(south_america, f)
    # with open ("../json/dated_settlements_geo.json", "w") as f:
    #     json.dump(world, f)
    with open ("../json/americas_d_geo.json", "w") as f:
        json.dump(americas, f)

    # Example object
    # { "type": "Feature",
    #     "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
    #     "properties": {"prop0": "value0"}
    #     },
         

if __name__ == "__main__":
    main()

