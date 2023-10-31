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
    37: [ "Liv",      "Marcus" ],
    38: [ "Sejr",     "Magnus" ],
    39: [ "Tobias",   "Jannick" ],
    40: [ "Laurits",  "Toke" ],
    41: [ "Viktor",   "Burak" ],
    43: [ "Noah",     "Philip" ],
    44: [ "Hazel",    "Thomas" ],
    45: [ "Sebastian","Martin" ],
    46: [ "Thor",     "Mads" ],
    47: [ "Mia",      "Holger" ],
    48: [ "Magne",    "Rasmus" ],
    49: [ "Lukas",    "Ksawery" ],
    50: [ "Thor",     "Philip" ],
    51: [ "Mads",     "Holger" ],
    1:  [ "Mia",      "Jannick" ],
    2:  [ "Thomas",   "Magne" ],
    3:  [ "Martin",   "Marcus" ],
    4:  [ "Laurits",  "Toke" ],
    5:  [ "Viktor",   "Sebastian" ],
    6:  [ "Lukas",    "Burak" ],
    8:  [ "Liv",      "Sejr" ],
    9:  [ "Noah",     "Magnus" ],
    10: [ "Rasmus",   "Ksawery" ],
    11: [ "Tobias",   "Hazel" ],
    12: [ "Thor",     "Philip" ],
    13: [ "Toke",     "Mads" ],
    14: [ "Magne",    "Laurits" ],
    15: [ "Rasmus",   "Sejr" ],
    16: [ "Burak",    "Magnus" ],
    17: [ "Holger",   "Noah" ],
    18: [ "Mia",      "Thomas" ],
    19: [ "Tobias",   "Martin" ],
    20: [ "Hazel",    "Sebastian" ],
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
    "Alexander":   "386838704184098818",
    "Cassandra":   "386838704184098818",
    "Burak":       "377142356354269184",
    "Flòra":       "727113666788327475",
    "Holger":      "444574998942711808",
    "Jannick":     "285867862588129283",
    "Hazel":       "318057147940470795",
    "Jesse":       "318057147940470795",
    "Rasmus":      "763332469654028328",
    "Ksawery":     "1042082836368343100",
    "Kasper":      "281387674588151808",
    "Laurits":     "590912103339130891",
    "Liv":         "907187868819148801",
    "Lukas":       "651332923911438340",
    "Mads":        "374086040874385412",
    "Magne":       "351795098075398145",
    "Magnus":      "431848896000425994",
    "Marcus":      "418799061571731458",
    "Martin":      "464712436528840725",
    "Mia":         "585394887176880128",
    "Noah":        "629682837804810270",
    "Philip":      "366147716851433474",
    "Sejr":        "518109475178020864",
    "Sebastian":   "405001313269710871",
    "Thomas":      "591616772818337802",
    "Thor":        "291897381341888513",
    "Tobias":      "216621385173172225",
    "Toke":        "366257424346251264",
    "Viktor":      "311544259662577675",
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
