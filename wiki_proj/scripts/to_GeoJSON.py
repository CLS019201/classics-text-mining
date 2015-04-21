# Converts our current JSON to GeoJSON in preparation for D3 map viz

import json

def main():
    new_data = {}
    new_data["type"] = "FeatureCollection"
    new_data["features"] = []
    with open("../json/settlements_locs.json","r") as f:
        raw_data = json.load(f)
        for entry in raw_data:
        	feature = {"type":"", 
        			   "geometry":{"coordinates":[]},
        			   "properties":{"type":"", "est_date":"", "ext_date":""}
        			   }
        	feature["type"] = "Feature"
        	feature["geometry"]["type"] = "Point"
        	feature["geometry"]["coordinates"] = [entry["lat"], entry["lng"]]

        	feature["properties"]["type"] = entry["_TYPE"]
        	feature["properties"]["type"] = entry["_TYPE"]
        	feature["properties"]["est_date"] = entry["established_date"]
        	feature["properties"]["ext_date"] = entry["extinct_date"]
        	new_data["features"].append(feature)
    with open ("../json/settlements_geo.json", "w") as f:
    	json.dump(new_data, f)

    # Example object
    # { "type": "Feature",
    #     "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
    #     "properties": {"prop0": "value0"}
    #     },
         

if __name__ == "__main__":
    main()

