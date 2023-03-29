from secrets import api_key
import requests
import json
import re

site_id = 354182
daily_weather_call = \
    f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/{site_id}?res=daily&key={api_key}" \
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
        night_rain_probability = json.dumps(
            api_response["SiteRep"]["DV"]["Location"]["Period"][counter]["Rep"][1]["PPn"])

        # The responses are enclosed in speech marks, so we must use regex to remove them.
        # We then convert the regex response to an integer
        # And finally add all the results to a list
        weather_types.append(int(re.sub("[^0-9]", "", day_weather_type)))
        weather_types.append(int(re.sub("[^0-9]", "", night_weather_type)))
        rain_probabilities.append(int(re.sub("[^0-9]", "", day_rain_probability)))
        rain_probabilities.append(int(re.sub("[^0-9]", "", night_rain_probability)))

    return weather_types, rain_probabilities


def is_weather_type_acceptable(weather_types):
    """ decides if weather is acceptable by looking at weather type

    To do this, we will check how many occurances of weather_types > 8 there are.
    If there are two occurances greater than 8, then we will class it as UNACCEPTABLE

    https://www.metoffice.gov.uk/services/data/datapoint/code-definitions

    :return True - acceptable weather
    :return False - unacceptable weather
    """
    gtr_8_occurances = 0
    for code in weather_types:
        if code > 8:
            gtr_8_occurances += 1

    return False if gtr_8_occurances > 1 else True

def decide_send_alert(bool_weather_type, bool_precipitation):
    """Decides whether to send email or not based on weather type and chance of rain"""

    return True if bool_weather_type is True and bool_precipitation is True else False

def is_precipitation_acceptable(rain_probabilities):
    """ decides if weather is acceptable by looking at precipitation probabilities

    True - avg rain < 30
    False - avg rain > 30
    """

    avg_precipitation = sum(rain_probabilities) / len(rain_probabilities)
    return False if avg_precipitation > 30 else True


def main():
    """this calls all the functions.  if is_weather_acceptable returns T, send email"""

    api_response = make_call(354182, daily_weather_call)
    weather_types, rain_probabilities = parse_data(api_response)
    bool_weather_type = is_weather_type_acceptable(weather_types)
    bool_precipitation = is_precipitation_acceptable(rain_probabilities)
    decide_send_alert(bool_weather_type, bool_precipitation)


main()
