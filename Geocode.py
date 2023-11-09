import requests     

# input = "800-BLK WILLIAMSON RD, IREDELL COUNTY"
def geocodeaddress(input):
    key = "APIKEYHERE"
    outputFormat = "json"
    addy = "address=" + input 
    url = "https://maps.googleapis.com/maps/api/geocode/" + outputFormat + "?" + addy + "&" + key

    response = requests.get(url)
    print(response.status_code) 

    if response.status_code == 200:
        data = response.json()
        if "results" in data and data["results"]:
            # Assuming you want the first result's latitude
            lat = data["results"][0]["geometry"]["location"]["lat"]
            print(lat)
            lng = data["results"][0]["geometry"]["location"]["lng"]
            print(lng)
            return lat, lng
        else:
            return None  # Handle the case where there are no results
    else:
        print("Request failed with status code:", response.status_code)
        return None  # Handle the request failure

# output = (geocodeaddress(input))

# print(output[0])



