# kyloe - 352624, middleton
# bowden- 352624, middleton
# back bowden- 352624, middleton
# whickam - 354182,Whickham Thorns Outdoor Centre
# corbys
# shaftoe
# crag lough
# peel crag
# simonside
# Ravensheugh

from secrets import api_key
import requests
import json
site_id = 354182

response = requests.get(
    f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/{site_id}?res=3hourly&key={api_key}"
    .format(site_id, api_key)).json()
print(json.dumps(response, indent=2))  # pretty prints response
