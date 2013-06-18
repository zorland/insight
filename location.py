import requests

def loc_APIString(address = '94305'):
    print 'strating'
#    gmaps = GoogleMaps('AIzaSyBRAegE--xWfdAJQCkehT6j1y0Ic_KOBik')
#    address = '94305'
#    lat, lng = gmaps.address_to_latlng(address)
#    print lat, ln
    return "http://maps.googleapis.com/maps/api/geocode/json?address="+address +"&sensor=true"
#http://maps.googleapis.com/maps/api/geocode/json?address=511+hamilton+evanston&sensor=true

#def find_loc2(address = '94305'):

#    results = Geocoder.geocode(address)
#    print(results[0].coordinates)
#    print(results[0])

def loc_FileThing(APIcall, filename = 'default_loc.txt'):

    r = requests.request("GET",APIcall)
    rawData = open(filename,"w")
    rawData.write(r.text)
    rawData.close()
    return


