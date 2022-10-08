#import pymouse
from datetime import datetime, timedelta
import Xlib
import Xlib.display
from pprint import pprint
import time
import json
import os
from status import Status
from misc import format_timedelta

from Xlib.ext import xinput

class RunescapeStatus(Status):
	
	def __init__(self):
		self.runescape_id = None
		self.display = Xlib.display.Display()
		self.runescape = None
		self.last_interact_time = datetime.now()
		self.last_click_time = datetime.now()
		self.last_query_time = time.time() - 10
		self.last_status = None
		self.interval = 3

	def get_runescape_window(self, j = None):
		if j is None:
			j = json.load(os.popen("i3-msg -t get_tree"))
		for node in j["nodes"]:
			#print(node["name"])
			if node["name"] == "RuneScape":
				return self.display.create_resource_object("window", node["window"])
			other = self.get_runescape_window(node)
			if other is not None:
				return other
		#exit("fail!")
		return None

	def handle_events(self):
		while self.display.pending_events() > 0:
			e = self.display.next_event()
			self.last_interact_time = datetime.now()
			if e._data.get("evtype") == xinput.ButtonRelease and (e.data.buttons._value & 1):
				self.last_click_time = datetime.now()

	def get_status(self):
		if self.last_query_time + self.interval >= time.time():
			return self.last_status
		runescape = self.get_runescape_window()
		if runescape is None:
			self.runescape = None
		elif self.runescape is None or self.runescape.id != runescape.id:
			self.runescape = runescape
			self.runescape.xinput_select_events([(xinput.AllDevices, xinput.MotionMask | xinput.ButtonReleaseMask)])
			self.last_interact_time = datetime.now()
			self.last_click_time = datetime.now()
		if runescape is None:
			self.last_status = None
		else:
			self.handle_events()
			interact_delta = (datetime.now() - self.last_interact_time)
			click_delta = (datetime.now() - self.last_click_time)
			normal_color = "#ffff77"
			warning_color = "#ff0000"
			should_warn = interact_delta >= timedelta(minutes=3)
			extra_text = ("BAD THINGS ARE COMING!" * 3 + " ") if (timedelta(minutes = 4, seconds = 30) <= interact_delta and interact_delta <= timedelta(minutes = 5, seconds = 10)) else ""
			self.last_status = [
				{
					"full_text" : f"RS ",
					"color" : warning_color if should_warn else normal_color,
					"separator_block_width" : 0,
				},
				{
					"full_text" : f"{extra_text}({format_timedelta(interact_delta)}) ",
					"color" : warning_color if should_warn else normal_color,
					"separator_block_width" : 0,
				},
				{
					"full_text" : f"({format_timedelta(click_delta)})",
					"color" : warning_color if should_warn or click_delta >= timedelta(minutes = 1) else normal_color,
				}
			]
		return self.last_status

if __name__ == "__main__":
	status = RunescapeStatus()
	while True:
		print(status.get_status())
		time.sleep(0.2)
