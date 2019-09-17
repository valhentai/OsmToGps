from geopy.geocoders import Nominatim

def getAreaOsmId(name):

    # Geocoding request via Nominatim
    geolocator = Nominatim(user_agent="city_compare")
    geo_results = geolocator.geocode(name, exactly_one=False, limit=3)

    # Searching for relation in result set
    for r in geo_results:
        if r.raw.get("osm_type") == "relation":
            city = r
            break

    # Calculating area id
    area_id = int(city.raw.get("osm_id")) + 3600000000
    print(str.format("found geo area {0} with id {1}",name,area_id))

    return area_id