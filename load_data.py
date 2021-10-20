import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim

df = pd.read_csv("flavors_of_cocoa.csv")
df.columns = ["company", "specific_location", "REF", "review_date", "cocoa_percentage", "company_location", "rating", "bean_type", "general_location"]

app = Nominatim(user_agent="tutorial")

lat = []
lon = []
print(df.company_location.unique())


for i in range(len(df.general_location)):
    try:
        location = app.geocode(df.general_location[i]).raw
        latitude = location["lat"]
        longitude = location["lon"]
        lat.append(latitude)
        lon.append(longitude)
        print(f"{latitude}, {longitude}")
    except:
        lat.append(0)
        lon.append(0)
        print(df.general_location[i])

df["lon"] = lon
df["lat"] = lat

df.to_csv("output.csv", index=False)