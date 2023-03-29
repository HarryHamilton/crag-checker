from secrets import api_key
import requests
import json

site_id = 354182
daily_weather_call = \
    f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/{site_id}?res=daily&key={api_key}"\
        .format(site_id, api_key)

def make_call(site_id, call):
    api_response = requests.get(daily_weather_call).json()
    return api_response

def parse_data(api_response):
    """We need to parse through the data 10 times.
    We get five days worth of data, each day giving us two things to look at (day n nite)"""


def is_weather_acceptable():
    """ decides if weather is acceptable by looking at weather type and Pp% """
    continue

def main():
    """this calls all of the functions.  if is_weather_acceptable returns T, send email"""

    api_response = make_call(354182, daily_weather_call)
    parse_data(api_response)
