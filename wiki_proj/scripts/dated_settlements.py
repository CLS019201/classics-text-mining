# grab settlements with dates:
import json
def main():
	dated = []
	with open("../json/settlements_locs.json", 'r') as f:
		locs = json.load(f)
		
		for entry in locs:
			if entry['established_date'] != "":
				dated.append(entry)
	with open("../json/dated_settlements_locs.json",'w') as f:
		json.dump(dated, f, indent=2)

if __name__ == "__main__":
	main()