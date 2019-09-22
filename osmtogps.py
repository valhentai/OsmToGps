import overpy
import os.path
import argparse
import name_to_area as nta
import subprocess
from linq import Flow, extension_std
import json


class OverpassApiItemProvider:
    
    def __init__(self, querypath, area):
        self.area = area

        self.query = readqueryfile(querypath)

        area_id = nta.getAreaOsmId(area)
        self.query = self.query.format(geoarea=str(area_id))

        api = overpy.Overpass()

        print("Query Overpass")
        # fetch all ways and nodes
        self.result = api.query(self.query)

    def generateitem(self,node):
        item = dict()
        item.update({"lon": node.lon})
        item.update({"lat": node.lat})
        item.update({"name": node.tags.get("name","")})
        return item

    def getitems(self):
        return Flow(self.result.nodes).Map(lambda n : self.generateitem(n)).Unboxed()


class GeojsonItemProvider:

    def __init__(self, path):
        self.data = None
        with open(path, 'r',encoding="utf8") as f:
           self.data = json.load(f)

    def generateitem(self,node):
        coords = node["geometry"]["coordinates"]
        if "name" in node["properties"]:
            name = node["properties"]["name"]
        else:
            name = ""
        item = dict()
        item.update({"lon": coords[0]})
        item.update({"lat": coords[1]})
        item.update({"name": name})
        return item
        

    def getitems(self):
        return Flow(self.data["features"]).Map(lambda n : self.generateitem(n)).Unboxed()



def readqueryfile(path):
    with open(path, "r",encoding="utf8") as f:
        return f.read()


parser = argparse.ArgumentParser(description='Query osm data and convert to TomTom POI file')
parser.add_argument('--query' ,dest="query",type=str)
parser.add_argument('--geoarea' ,dest="geoarea",type=str)

parser.add_argument('--geojson' ,dest="geojson",type=str)

args = parser.parse_args()



if args.query is not None:
    filename =  args.query
    overpassquery = OverpassApiItemProvider(args.query,args.geoarea)
    items =  overpassquery.getitems()

if args.geojson is not None:
    filename =  args.geojson
    provider = GeojsonItemProvider(args.geojson)
    items =  provider.getitems()

plainpath = "output/"+os.path.basename(filename)+".out.txt"
print("Store result in "+plainpath)
plaintxtout = open(plainpath,"w",encoding="utf8") 

for item in items:
    plaintxtout.write(str.format("{0} , {1} , {2} \n",item["lon"],item["lat"],item["name"]))

plaintxtout.close()

outov2 = "output/"+os.path.basename(filename)+".ov2"
cmd = str.format("ov2tools/makeov2.exe {0} {1}",plainpath,outov2)
print("convert to ov2")
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
process.wait()

