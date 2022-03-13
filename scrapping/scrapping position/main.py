
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
from requests import get


places = dict()
response = get("https://www2.assemblee-nationale.fr/deputes/hemicycle").text

soup = BeautifulSoup(response, 'html.parser')
data = soup.find("div",{"id":"data"})

deputes = data.find_all("dl")
for d in deputes:
    places[int(d["data-place"][1:])] = {"nom":d["data-nom"]}

#print(places)

f = open("hemi.js", "r")

paths = dict()

for line in f.readlines():
    if line.find("hemi") != -1:
        parts = line.split("hemi")
        paths[parts[1][2:5]]=parts[2].split("\"")[1]

def parse_num(num,end=0):
    try:
        int(num)
        return int(num)
    except:
        if len(num)>1:
            return parse_num(num[:-1])

for key in paths:
    pointsPrint = paths[key].split(" ")
    del pointsPrint[0]
    points = []
    for point in pointsPrint:
        if len(point.split(","))<=1:
            break
        x,y = point.split(",")
        points.append([float(x),float(y)])

    x = points[0][0]+(points[1][0]+points[2][0]+points[3][0])/2
    y = points[0][1] + (points[1][1] + points[2][1] + points[3][1]) / 2
    place = parse_num(key)
    if places.get(place):
        places[place]["position"]=[x,y]

for place in places:
    print(places[place])
    plt.plot(places[place]["position"][0],places[place]["position"][1], 'o', color='black')

plt.show()

json_string = json.dumps(places, indent=4, sort_keys=True,ensure_ascii=False)
with open('results.json', 'w') as outfile:
    outfile.write(json_string)

