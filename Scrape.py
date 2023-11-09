from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import sys 
import folium
from datetime import datetime, timedelta
from Geocode import geocodeaddress



# #EXTRACTS DAT FROM FRONT END

# op = webdriver.ChromeOptions()
# op.add_argument('--headless')

# driver = webdriver.Chrome(options = op)
# driver.get('http://152.31.128.153/Summary.aspx')

# # Click "Agree" on the terms and conditions
# termsagree = driver.find_element(By.XPATH, '//*[@id="mainContent_CenterColumnContent_btnContinue"]')
# termsagree.click()

# # Click "Search"
# search = driver.find_element(By.XPATH, '//*[@id="mainContent_cmdSubmit2"]/span[2]')
# search.click()

# # Attempts to locate the data
# # If no new data is present, will error and exit
# try:
#     table = driver.find_element(By.XPATH, '//*[@id="mainContent_gvSummary"]')
# except NoSuchElementException:
#     print("No new data")
#     driver.quit()
#     sys.exit()









# # GEOCODES ADDRESS DATA AND FORMATS IT FOR GEOJSON

# # Extract the data for the created list and convert it into a dictionary
# table_data = []

# rows = table.find_elements(By.TAG_NAME, 'tr')

# for row in rows:
#     columns = row.find_elements(By.TAG_NAME, 'td')
#     row_data = [column.text for column in columns]
#     # Check if row_data contains enough elements
#     if len(row_data) >= 5:
#         # Geocode the address
#         input_address = row_data[4] + ", IREDELL COUNTY, NC"
#         geo_out = geocodeaddress(input_address)
#         lat = geo_out[0]
#         lng = geo_out[1]

#         # Create a dictionary with data
#         convert_dict = {
#       "type": "Feature",
#       "geometry": {
#         "type": "Point",
#         "coordinates": [lng, lat]
#       },
#       "properties": {
#         "Date": row_data[1],
#         "Primary Offense": row_data[3],
#         "Address1": row_data[4]
#       }
#     }
#         table_data.append(convert_dict)










# # APPENDS NEW DATA AND CLEANS OUT OLD DATA



# # Load existing test data (if any)
# with open("MapData.json", "r") as json_file:
#     existing_data = json.load(json_file)

# # Append the new data to the existing test data
# existing_data["features"].extend(table_data)

# # Define a function to check if a date is more than 30 days old
# def is_old_date(date_string):
#     date = datetime.strptime(date_string, "%m/%d/%Y %H:%M")
#     today = datetime.now()
#     thirty_days_ago = today - timedelta(days=30)
#     return date < thirty_days_ago

# # Filter out features with dates more than 30 days old
# existing_data["features"] = [feature for feature in existing_data["features"] if not is_old_date(feature["properties"]["Date"])]

# # Save the updated data back to the JSON file
# with open("MapData.json", "w") as json_file:
#     json.dump(existing_data, json_file, indent=4)

# print("Data update complete")























# UPDATING THE HTML WITH THE NEW DATA 



# Load the GeoJSON data
with open("MapData.json", "r") as json_file:
    geojson_data = json.load(json_file)

# Load the iredell county bounadry line geojson
with open("IRE BOUND.geojson", "r") as boundary_line:
    boundary_line = json.load(boundary_line)



# Define stlying for the boundary line
style_function_bound = lambda feature: {
        "color": "black",
        "weight": 2
    }





# Define styling and popup fields for markers that create 
style_function_marker=lambda feature: {
        "opacity": '1.0' if feature["properties"]["Date"] > datetime.strftime(datetime.now() - timedelta(days=3), "%m/%d/%Y %H:%M") else "0.5"
    }
marker=folium.Marker(fill_color="orange")
popup=folium.GeoJsonPopup(fields=["Date", "Primary Offense"])


# Create a map, add GeoJSON data, and display it
map_center = [35.791723, -80.882428]
m = folium.Map(location=map_center, zoom_start=10)
folium.GeoJson(geojson_data, marker=marker, style_function=style_function_marker, popup=popup).add_to(m)
folium.GeoJson(boundary_line, style_function=style_function_bound).add_to(m)
m.save("MapDisplay.html")

print("Updated HTML")
