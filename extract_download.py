import download_helper
import os.path as path
import os

def download_extract(continent,country):

    url = "http://download.openstreetmap.fr/extracts/"
    datapath = "data"
    datapath = path.join(datapath,continent)
    url = url + continent.lower()
    if not os.path.exists(datapath):
        os.makedirs(datapath)
    datapath = path.join(datapath,country.lower()+ "-latest.osm.pbf")
    url = url + "/" + country.lower() + "-latest.osm.pbf"

    download_helper.download(url, datapath)

download_extract("europe","France")