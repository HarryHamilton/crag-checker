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
    """We need to parse through the data 8 times.
    We want 4 days worth of data (inc today), each day giving us two things to look at (day n nite)"""

    weather_types = []  # list containing all the weather types for the next 72 hours
    rain_probabilities = []  # list containing % chance of rain for the next 72 hours
    for counter in range(4):
        day_weather_type = json.dumps(api_response["SiteRep"]["DV"]["Location"]["Period"][counter]["Rep"][0]["W"])
        night_weather_type = json.dumps(api_response["SiteRep"]["DV"]["Location"]["Period"][counter]["Rep"][1]["W"])
        day_rain_probability = json.dumps(api_response["SiteRep"]["DV"]["Location"]["Period"][counter]["Rep"][0]["PPd"])
        night_rain_probability = json.dumps(api_response["SiteRep"]["DV"]["Location"]["Period"][counter]["Rep"][1]["PPn"])

        weather_types.append(day_weather_type)
        weather_types.append(night_weather_type)
        rain_probabilities.append(day_rain_probability)
        rain_probabilities.append(night_rain_probability)

    return weather_types, rain_probabilities


def is_weather_acceptable():
    """ decides if weather is acceptable by looking at weather type and Pp% """

def main():
    """this calls all of the functions.  if is_weather_acceptable returns T, send email"""

    api_response = make_call(354182, daily_weather_call)
    parse_data(api_response)


