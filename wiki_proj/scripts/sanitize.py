### sanitize.py
__USEFUL_FLAGS = ['latd', 'longd', 'longitude', 'latitude', 'coord', 'CoorHeader',
                  'coor d', 'Geolinks', 'Mapit', '| loc', 'coor_pinpoint', 'coordinates_',
                  'common_name','established_date','_date', 'official_name', 'settlement_type',
                  '_type', '| name', '|name', '| lat', '| long', '|lat', '|long', 'coor_', '_type',
                  'infobox', 'Infobox', 'latm','longm','lats','longs','latN','longE']

def main():
  with open ("../results/sanitize1.xml","w") as wf:
      wf.write("")

  with open ("../results/sanitize1.xml","a") as wf:
      with open("../results/all_infoboxes.xml","r") as f:
          for line in f:
              if any(key in line for key in __USEFUL_FLAGS):
                  wf.write(line)

if __name__ == "__main__":
    main()