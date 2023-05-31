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
    11: ["***REMOVED***", "***REMOVED***"],
    12: ["***REMOVED***", "***REMOVED***"],
    13: ["***REMOVED***", "***REMOVED***"],
    15: ["***REMOVED***", "***REMOVED***"],
    16: ["***REMOVED***", "***REMOVED***"],
    17: ["***REMOVED***", "***REMOVED***"],
    18: ["***REMOVED***", "***REMOVED***"],
    19: ["***REMOVED***", "***REMOVED***"],
    20: ["***REMOVED***", "***REMOVED***"],
    21: ["***REMOVED***", "***REMOVED***"],
    22: ["***REMOVED***", "***REMOVED***"]
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
    "***REMOVED***":  "386838704184098818",
    "***REMOVED***":  "386838704184098818",
    "***REMOVED***":              "377142356354269184",
    "***REMOVED***":                  "727113666788327475",
    "***REMOVED***":                 "444574998942711808",
    "***REMOVED***":              "285867862588129283",
    "***REMOVED***":          "318057147940470795",
    "***REMOVED***":               "763332469654028328",
    "***REMOVED***":                  "1042082836368343100",
    "***REMOVED***":       "281387674588151808",
    "***REMOVED***":        "590912103339130891",
    "***REMOVED***":          "907187868819148801",
    "***REMOVED***":             "651332923911438340",
    "***REMOVED***":          "374086040874385412",
    "***REMOVED***":         "351795098075398145",
    "***REMOVED***":             "431848896000425994",
    "***REMOVED***":       "418799061571731458",
    "***REMOVED***":     "464712436528840725",
    "***REMOVED***": "585394887176880128",
    "***REMOVED***":            "629682837804810270",
    "***REMOVED***":         "366147716851433474",
    "***REMOVED***":             "518109475178020864",
    "***REMOVED***":    "405001313269710871",
    "***REMOVED***":            "591616772818337802",
    "***REMOVED***":       "291897381341888513",
    "***REMOVED***":           "216621385173172225",
    "***REMOVED***":           "366257424346251264",
    "***REMOVED***":   "311544259662577675",
}

def try_mention(name):
    try:
        id = name_to_id[name]
        return f"{name} (<@{id}>)"
    except KeyError:
        return name

mentions = [try_mention(n) for n in names]

concatenated_mentions = ", ".join(mentions[:-1]) + " og " + mentions[-1]

message = f"Der er IT hjælp i lokale D4407\n(dagens dukse er {concatenated_mentions}\nnu vil jeg ikke have nogen skipperering fra jer gutter og mia!)"

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
