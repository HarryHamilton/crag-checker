https://www.metoffice.gov.uk/services/data/datapoint/code-definitions

https://www.metoffice.gov.uk/services/data/datapoint/api-reference#textual-data

{
          "name": "F",
          "units": "C",
          "$": "Feels Like Temperature"
        },
        {
          "name": "G",
          "units": "mph",
          "$": "Wind Gust"
        },
        {
          "name": "H",
          "units": "%",
          "$": "Screen Relative Humidity"
        },
        {
          "name": "T",
          "units": "C",
          "$": "Temperature"
        },
        {
          "name": "V",
          "units": "",
          "$": "Visibility"
        },
        {
          "name": "D",
          "units": "compass",
          "$": "Wind Direction"
        },
        {
          "name": "S",
          "units": "mph",
          "$": "Wind Speed"
        },
        {
          "name": "U",
          "units": "",
          "$": "Max UV Index"
        },
        {
          "name": "W",
          "units": "",
          "$": "Weather Type"
        },
        {
          "name": "Pp",
          "units": "%",
          "$": "Precipitation Probability"
        }
      ]
    },


Useful points:
 - weather type ("W")
 - precipitation probability ("Pp")
 - wind speed ("s")


know different "res":
- 3hourly
- daily

["SiteRep"]["DV"]["Location"]["Period"][TODAY(0), TOMORROW(1) ETC]["Rep"][DAY (0), NIGHT (1)][CODE (E.G. "PP" FOR PRECICIPATION)]

#print(json.dumps(response, indent=2))  # pretty prints response
#print(json.dumps(api_response["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"], indent=2))  # print just the forecast for today
#print(json.dumps(api_response["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"][0], indent=2))  # DAY forcast for TODAY
son.dumps(api_response["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"][0]["W"], indent=2)) # weather type for DAY forecast for TODAY



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


How to determine whether to send email or not:
1) have a list of acceptable day & night weather types:
   - any weather type < 9 is acceptable2
2) any avg precipitation probability < 30 is acceptable
3) So, if weathertype < 9 and Pp < 20, send email.


What an email will contain:
1) Date/time that the weather was checked (this is found at top of api call i think)
2) met office location that was searched (e.g. "middleton" for bowden)
3) actual name of crag
4) weather type (convert number to words using that list in useful_links.md)
5) chance of rain (simply Pp%)
6) wind speed


