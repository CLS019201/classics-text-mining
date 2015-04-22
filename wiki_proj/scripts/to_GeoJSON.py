# Converts our current JSON to GeoJSON in preparation for D3 map viz

import json

def main():
    new_data = {}
    new_data["type"] = "FeatureCollection"
    new_data["features"] = []
    america = new_data
    south_america = new_data
    with open("../json/settlements_locs.json","r") as f:
        raw_data = json.load(f)
        stop = 0
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
        	# if entry["lat"] >= 24 and entry["lat"] <= 50 and -125 <= entry["lng"] and entry["lng"] <= -66:
	        # 	america["features"].append(feature)
        	if entry["lat"] >= -57 and entry["lat"] <= 14 and -94 <=entry["lng"] and entry["lng"] <= -32:
        		south_america["features"].append(feature)
        	if(entry["lat"] >= 0) and (entry["lat"] <= 0):
        		america["features"].append(feature)
    with open ("../json/america.json", "w") as f:
    	json.dump(america, f)
    with open ("../json/south_america.json", "w") as f:
    	json.dump(south_america, f)

    # Example object
    # { "type": "Feature",
    #     "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
    #     "properties": {"prop0": "value0"}
    #     },
         

if __name__ == "__main__":
    main()

