import json, operator, re
from bs4 import BeautifulSoup

good_classes = []
xml_db = "sanitize_1.xml"
with open ("list_attr.json", "r") as f:
    pairs = json.load(f)
    for tup in pairs:
        good_classes.append(tup[0])

with open ("class_list.json", "w") as f:
    json.dump(good_classes,f)

soup =  BeautifulSoup(open("sanitize_1.xml"))

def dump_boxes_of_class(c):
    class_boxes = soup.find_all('infobox', c)
    print class_boxes
    with open("classes_xml/"+c+".xml","a") as f:
        for doc in class_boxes:
            f.write(doc.string, encoding="utf-8")
dump_boxes_of_class("American")



