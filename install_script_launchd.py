"""This script installs the bot as a Launchd job on MacOS."""

from os.path import abspath, dirname
from sys import executable
from time import sleep
import launchd
import os

project_root = dirname(abspath(__file__))

logfile = "/tmp/duksebot.log"

label = "local.duksebot"

plist = {
    "Label": label,
    "ProgramArguments": [
        executable,
        f"{project_root}/script.py"
    ],
    "ServiceDescription": "Underretter dagens dukse om deres skæbne >:)",
    "StartCalendarInterval": [
        { "Hour": 8, "Weekday": w } for w in (0, 1, 2, 3, 4, 5)
    ],
    "StandardInPath": logfile,
    "StandardOutPath": logfile,
    "StandardErrorPath": logfile,
}

job = launchd.LaunchdJob(label)
if not job.exists():
    print(f"'{label}' is not loaded in launchd. Installing...")
    fname = launchd.plist.write(label, plist, scope=launchd.plist.USER)
    launchd.load(fname)
    while job.pid is not None:
        print("Alive! PID = %s" % job.pid)
        job.refresh()
        sleep(0.2)
else:
    print("Uninstalling again...")
    fname = launchd.plist.discover_filename(label)
    assert fname is not None
    launchd.unload(fname)
    os.unlink(fname)
