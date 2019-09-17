import overpy
import os.path
import argparse
import name_to_area as nta
import subprocess

def readqueryfile(path):
    with open(path, "r",encoding="utf8") as f:
        return f.read()

parser = argparse.ArgumentParser(description='Query osm data and convert to TomTom POI file')
parser.add_argument('--query' ,dest="query",type=str)
parser.add_argument('--geoarea' ,dest="geoarea",type=str)

args = parser.parse_args()
query = readqueryfile(args.query)

area_id = nta.getAreaOsmId(args.geoarea)

query = query.format(geoarea=str(area_id))

api = overpy.Overpass()

print("Query Overpass")
# fetch all ways and nodes
result = api.query(query)

plainpath = "output/"+os.path.basename(args.query)+".out.txt"
print("Store result in "+plainpath)
plaintxtout = open(plainpath,"w",encoding="utf8") 

for node in result.nodes:
    plaintxtout.write(str.format("{0} , {1} , {2} \n",node.lon,node.lat,node.tags.get("name","")))

plaintxtout.close()

outov2 = "output/"+os.path.basename(args.query)+".ov2"
cmd = str.format("ov2tools/makeov2.exe {0} {1}",plainpath,outov2)
print("convert to ov2")
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
process.wait()

