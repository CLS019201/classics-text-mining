### sanitize.py
__USEFUL_FLAGS = ['latd', 'longd', 'longitude', 'latitude', 'coord', 'CoorHeader',
                  'coor d', 'Geolinks', 'Mapit', '| loc', 'coor_pinpoint', 'coordinates_',
                  'common_name','established_date','_date', 'official_name', 'settlement_type',
                  '_type', '| name', '|name', '| lat', '| long', '|lat', '|long', 'coor_', '_type', 'infobox', 'Infobox']

def has_good_info(line):
    if any(key in line for key in __USEFUL_FLAGS):
        return True
    else:
        return False

with open ("../results/sanitize_1.xml","w", encoding='utf-8') as wf:
    wf.write("")

with open ("../results/sanitize_1.xml","a", encoding='utf-8') as wf:
    with open("../results/example_out_500.xml","r", encoding='utf-8') as f:
        for line in f:
            if has_good_info(line):
                wf.write(line)