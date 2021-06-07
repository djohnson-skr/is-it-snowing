from pprint import pprint
from datetime import date
import requests
import yagmail


# Get request to OpenWeather API to get a 7 day forecast (Daily Forecast 7 days)
r = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=40.1573&lon=-76.3069'
                 '&units=metric&exclude=hourly,minutely&appid=bec19aebae773dbd42f7ce6d2fcd2b7f')


# Check to see if the request was successful
if r.status_code != 200:
    print('There was an issue with the get request')
    exit()
else:
    pass

info = r.json()  # .json() shows us the data the we got from the request (got it in JSON format)
#pprint(info['daily'][0])  # instead of using json.dumps we can use pprint to get a sense of how the data looks


# Check to see if it is actually going to be snowing today
def snowing():
    if info['daily'][0]['weather'][0]['main'] == 'Snow':
        return True
    else:
        False
        print("It aint gunna snow")

# yagmail.register('<email address>', '<password>')
# This registers the username and password to your OS'
# keyring allows you to instantiate the client by simply passing your username, e.g. yagmail.SMTP('myemailusername')
# Upon initial register make sure to import keyring


# If it is going to be snowing then send the email
if snowing():
    # -----PARAMETERS-------
    snowfall = info['daily'][0]['snow']
    dayTemp = info['daily'][0]['temp']['day']
    nightTemp = info['daily'][0]['temp']['night']
    windSpeed = round(info['daily'][0]['wind_speed'] * 3.6, 1)  # converting from m/s to kph and round to 1 decimal
    date = date.today()

    yag = yagmail.SMTP('<eamil address>, '<email password>')  # Start a connection
    receivers = ['<enter email passwords>']  # Recipients of the email
    body = '<h1>Welcome to Ultimate Weather!</h1>' \
           'Thank you for subscribing to your personalized weather reports by the hour provided by' \
           ' yaweatherboi!\n' \
           'It looks like you got some good ole snow coming your way! If you give your best snow dance ' \
           'you can expect up to %s cm of snow today!\n\n' \
           '<p style="font-weight: bold;">Your Daily Trackers:</p>' \
           'Daytime Temperature: %s°C\n' \
           'Nighttime Temperature: %s°C\n' \
           'Wind Speed: %s kph\n\n\n' % (snowfall, dayTemp, nightTemp, windSpeed)

    for receiver in receivers:  # Loop through each recipient to send an individual email
        yag.send(
            to=receiver,
            subject="Weather Report for " + str(date),
            contents=body
        )

    print('Emails sent')
else:
    exit()

