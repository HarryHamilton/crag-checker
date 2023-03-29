from secrets import api_key, sender, email_password
import requests
import json
import re
from datetime import datetime
# email stuff
from mail_recipients import mail_recipients
from email.message import EmailMessage
import ssl
import smtplib


sites = {
    "Kyloe": 352624,
    "Bowden": 352624,
    "Whickham": 354182,
    "Corbys": 0,
    "Shaftoe": 0,
    "Crag Lough": 0,
    "Corbys": 0,
    "Simonside": 0,
    "Ravensheugh": 0,
}

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
    now = datetime.now()
    for counter in range(4):
        metoffice_location = json.dumps(api_response["SiteRep"]["DV"]["Location"]["name"])
        date_time_checked = json.dumps(api_response["SiteRep"]["DV"]["Location"]["Period"][0]["value"])\
                            + now.strftime("%H:%M%S")
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

    return weather_types, rain_probabilities, metoffice_location, date_time_checked


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


def is_precipitation_acceptable(rain_probabilities):
    """ decides if weather is acceptable by looking at precipitation probabilities

    True - avg rain < 30
    False - avg rain > 30
    """

    avg_precipitation = sum(rain_probabilities) / len(rain_probabilities)
    return False if avg_precipitation > 30 else True


def decide_send_alert(bool_weather_type, bool_precipitation):
    """Decides whether to send email or not based on weather type and chance of rain"""

    return True if bool_weather_type is True and bool_precipitation is True else False


def send_email(crag_name, metoffice_location, avg_weather, avg_precipitation, avg_windspeed, date_time_checked):
    subject = f"Weather looks good at {crag_name} | Crag Checker".format(crag_name)
    body = f"""
    Crag: {crag_name}
    Met office location used: {metoffice_location}
    Average weather over the next 72 hours: {avg_weather}
    Average chance of rain over the next 72 hours: {avg_precipitation}
    Average wind speed over the next 72 hours: {avg_windspeed}
    Date/time checked: {date_time_checked}
    
    go send""".format(crag_name, metoffice_location, avg_weather, avg_precipitation, avg_windspeed, date_time_checked)

    em = EmailMessage()
    em["From"] = sender
    em["To"] = mail_recipients
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()  # security stuff

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, email_password)
        smtp.sendmail(sender, mail_recipients, em.as_string())


def main():
    """this calls all the functions.  if is_weather_acceptable returns T, send email"""

    api_response = make_call(354182, daily_weather_call)
    weather_types, rain_probabilities, metoffice_location, date_time_checked = parse_data(api_response)
    bool_weather_type, avg_weather_type = is_weather_type_acceptable(weather_types)
    bool_precipitation, avg_precipitation = is_precipitation_acceptable(rain_probabilities)
    decide_send_alert(bool_weather_type, bool_precipitation)
    send_email("crag_name", metoffice_location, avg_weather_type, avg_precipitation, "avg_windspeed", date_time_checked)

main()
