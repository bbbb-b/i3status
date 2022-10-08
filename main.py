#!/usr/bin/python3
from runescape_status import RunescapeStatus
from spotify_status import SpotifyStatus
from time_status import TimeStatus
from vm_status import VMStatus
from headphone_battery_status import HeadphoneBatteryStatus
import json
import time
import sys

all_status = list(map(lambda x : x(), [RunescapeStatus, VMStatus, SpotifyStatus, TimeStatus]))
init = {
	"version" : 1,
	#"seperator" : "|"
}
print(json.dumps(init))
print("[")
while True:
	d = []
	for it in map(lambda x : x.get_status(), all_status):
		if isinstance(it, list):
			d.extend(it)
		elif isinstance(it, dict):
			d.append(it)
	#d = json.dumps([*filter(lambda x : x != None, map(lambda x : x.get_status(), all_status))])
	print(json.dumps(d))
	print(",")
	sys.stdout.flush()
	sys.stderr.flush()
	time.sleep(0.05)


