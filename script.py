import datetime
import dotenv
import os
import pytz
import requests
import sys

## Config

dotenv.load_dotenv()

# The id of the webhook to use.
WEBHOOK_ID = os.environ["WEBHOOK_ID"]

# The token of the webhook to use.
WEBHOOK_TOKEN = os.environ["WEBHOOK_TOKEN"]

# A mapping from week numbers to lists of names. This is used
# to look up, whose turn it is.
week_to_suckers = {
    11: ["Lukas Skjødt Ibsen", "Alexander Leondré Høj Nielsen"],
    12: ["Viktor Henry Englyst Hasager", "Noah Bruncke Jensen"],
    13: ["Thomas Kjær Schmidt", "Toke Børresen Kramer"],
    15: ["Martin Emil Gribsholt-Beck", "Magne Barslev Pedersen"],
    16: ["Marcus Iversen Dalentoft", "Flòra Földesi"],
    17: ["Holger Windahl", "Jannick Rask Lyng"],
    18: ["Magnus Lund Borges", "Tobias Knage Thomsen"],
    19: ["Thor Hornshøj-Schierbeck", "Sejr Lytje Oehlers"],
    20: ["Ksawery Szmyt", "Jesse Benjamin Witzel"],
    21: ["Liv Brunsgaard Friman", "Laurits Linderoth Lolck"],
    22: ["Mia Jenny Rosenkrands Petersen", "Burak Kenan Tural"]
}

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

# Time zone to use for current week.
TIMEZONE = "Europe/Copenhagen"

## Who's turn is it?

time_zone = pytz.timezone(TIMEZONE)
today = datetime.datetime.now(time_zone).date()
try:
    week = today.isocalendar().week
except IndexError:
    print("No suckers for this week. Exiting.")
    sys.exit(0)

names = week_to_suckers[week]

## Construct message

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

url = f"https://discord.com/api/webhooks/{WEBHOOK_ID}/{WEBHOOK_TOKEN}"

data = {
        "username": "Duksebot",
        "content": message,
}

response = requests.post(url, json=data)
response.raise_for_status()
