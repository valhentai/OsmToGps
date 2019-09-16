import overpy
import os.path
import argparse

def readqueryfile(path):
    with open(path, "r") as f:
        return f.read()

parser = argparse.ArgumentParser(description='Query osm data and convert to TomTom POI file')
parser.add_argument('--query' ,dest="query",type=str)

args = parser.parse_args()
query = readqueryfile(args.query)

api = overpy.Overpass()

# fetch all ways and nodes
result = api.query(query)

for node in result.nodes:
    print("Name: %s" % node.tags.get("name", "n/a"))