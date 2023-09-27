import datetime
import dotenv
import icalevents.icalevents
import os
import pytz
import requests
import sys

## Check if school's out.

# Url of school events. This should point to a .ics file which lists all
# lessons as events.

CALENDAR_URL = "https://outlook.office365.com/owa/calendar/897dca157a1542f6b5755e6c2676a5c7@edu.aarhustech.dk/5d9bcd18c06b4dffad68112b87b847de8355939558013369796/S-1-8-3277253076-3182863098-1525276079-582714796/reachcalendar.ics"

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
events = icalevents.icalevents.events(CALENDAR_URL, start=today, end=tomorrow)

if len(events) == 0:
    print("There are no calendar events today -> stopping execution.")
    sys.exit(0)

## Who's turn is it?

# A mapping from week numbers to lists of names. This is used
# to look up, whose turn it is.
week_to_suckers = {
    37: [ "Liv Brunsgaard Friman", "Marcus Iversen Dalentoft" ],
    38: [ "Sejr Lytje Oehlers", "Magnus Lund Borges" ],
    39: [ "Tobias Knage Thomsen", "Jannick Rask Lyng" ],
    40: [ "Laurits Linderoth Lolck", "Toke Børresen Kramer" ],
    41: [ "Viktor Henry Englyst Hasager", "Burak Kenan Tural" ],
    43: [ "Noah Bruncke Jensen", "Philip Skytte Fuglsang" ],
    44: [ "Jesse Benjamin Witzel", "Thomas Kjær Schmidt" ],
    45: [ "Sebastian Sortkær Fomsgaard", "Martin Emil Gribsholt-Beck" ],
    46: [ "Thor Hornshøj-Schierbeck", "Mads Hyldgaard Jensen" ],
    47: [ "Mia Jenny Rosenkrands Petersen", "Holger Windahl" ],
    48: [ "Magne Barslev Pedersen", "Rasmus Høtbjerg Henriksen" ],
    49: [ "Lukas Skjødt Ibsen", "Ksawery Szmyt" ],
    50: [ "Thor Hornshøj-Schierbeck", "Philip Skytte Fuglsang" ],
    51: [ "Mads Hyldgaard Jensen", "Holger Windahl" ],
    1: [ "Mia Jenny Rosenkrands Petersen", "Jannick Rask Lyng" ],
    2: [ "Thomas Kjær Schmidt", "Magne Barslev Pedersen" ],
    3: [ "Martin Emil Gribsholt-Beck", "Marcus Iversen Dalentoft" ],
    4: [ "Laurits Linderoth Lolck", "Toke Børresen Kramer" ],
    5: [ "Viktor Henry Englyst Hasager", "Sebastian Sortkær Fomsgaard" ],
    6: [ "Lukas Skjødt Ibsen", "Burak Kenan Tural" ],
    8: [ "Liv Brunsgaard Friman", "Sejr Lytje Oehlers" ],
    9: [ "Noah Bruncke Jensen", "Magnus Lund Borges" ],
    10: [ "Rasmus Høtbjerg Henriksen", "Ksawery Szmyt" ],
    11: [ "Tobias Knage Thomsen", "Jesse Benjamin Witzel" ],
    12: [ "Thor Hornshøj-Schierbeck", "Philip Skytte Fuglsang" ],
    13: [ "Toke Børresen Kramer", "Mads Hyldgaard Jensen" ],
    14: [ "Magne Barslev Pedersen", "Laurits Linderoth Lolck" ],
    15: [ "Rasmus Høtbjerg Henriksen", "Sejr Lytje Oehlers" ],
    16: [ "Burak Kenan Tural", "Magnus Lund Borges" ],
    17: [ "Holger Windahl", "Noah Bruncke Jensen" ],
    18: [ "Mia Jenny Rosenkrands Petersen", "Thomas Kjær Schmidt" ],
    19: [ "Tobias Knage Thomsen", "Martin Emil Gribsholt-Beck" ],
    20: [ "Jesse Benjamin Witzel", "Sebastian Sortkær Fomsgaard" ],
}

# Time zone to use for current week.
TIMEZONE = "Europe/Copenhagen"

time_zone = pytz.timezone(TIMEZONE)
today = datetime.datetime.now(time_zone).date()
try:
    week = today.isocalendar().week
except IndexError:
    print("No suckers for this week. Exiting.")
    sys.exit(0)

names = week_to_suckers[week]

## Construct message

# A mapping from names to user ids. This is used to ping members.
name_to_id = {
    "Alexander Leondré Høj Nielsen":  "386838704184098818",
    "Cassandra Leondré Høj Nielsen":  "386838704184098818",
    "Burak Kenan Tural":              "377142356354269184",
    "Flòra Földesi":                  "727113666788327475",
    "Holger Windahl":                 "444574998942711808",
    "Jannick Rask Lyng":              "285867862588129283",
    "Jesse Benjamin Witzel":          "318057147940470795",
    "Rasmus Henriksen":               "763332469654028328",
    "Ksawery Szmyt":                  "1042082836368343100",
    "Kasper Kirstejn Johansen":       "281387674588151808",
    "Laurits Linderoth Lolck":        "590912103339130891",
    "Liv Brunsgaard Friman":          "907187868819148801",
    "Lukas Skjødt Ibsen":             "651332923911438340",
    "Mads Hyldgaard Jensen":          "374086040874385412",
    "Magne Barslev Pedersen":         "351795098075398145",
    "Magnus Lund Borges":             "431848896000425994",
    "Marcus Iversen Dalentoft":       "418799061571731458",
    "Martin Emil Gribsholt-Beck":     "464712436528840725",
    "Mia Jenny Rosenkrands Petersen": "585394887176880128",
    "Noah Bruncke Jensen":            "629682837804810270",
    "Philip Skytte Fuglsang":         "366147716851433474",
    "Sejr Lytje Oehlers":             "518109475178020864",
    "Sebastian Sortkær Fomsgaard":    "405001313269710871",
    "Thomas Kjær Schmidt":            "591616772818337802",
    "Thor Hornshøj-Schierbeck":       "291897381341888513",
    "Tobias Knage Thomsen":           "216621385173172225",
    "Toke Børresen Kramer":           "366257424346251264",
    "Viktor Henry Englyst Hasager":   "311544259662577675",
}

def try_mention(name):
    try:
        id = name_to_id[name]
        return f"{name} (<@{id}>)"
    except KeyError:
        return name

mentions = [try_mention(n) for n in names]

concatenated_mentions = ", ".join(mentions[:-1]) + " og " + mentions[-1]

message = f"""dagens dukse er {concatenated_mentions}
nu vil jeg ikke have nogen skipperering fra jer gutter (og mia!) :nerd:"""

## Send data

# Read secrets from `.env`.
dotenv.load_dotenv()

# The id of the webhook to use.
WEBHOOK_ID = os.environ["WEBHOOK_ID"]

# The token of the webhook to use.
WEBHOOK_TOKEN = os.environ["WEBHOOK_TOKEN"]

url = f"https://discord.com/api/webhooks/{WEBHOOK_ID}/{WEBHOOK_TOKEN}"

data = {
        "username": "Duksebot",
        "content": message,
}

response = requests.post(url, json=data)
response.raise_for_status()
