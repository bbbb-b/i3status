import os
import sys
from status import Status
import subprocess 
import time
import random
from pprint import pprint

class HeadphoneBatteryStatus(Status):
	def __init__(self):
		self.last_query_time = -10
		self.last_value = None
		self.last_error_value = None
		self.last_error = ""
		self.query_interval = os.getpid() % 5

	def get_battery(self):
		cmd = "gatttool -b 00:1B:66:C1:62:4F --char-read -u 00002a19-0000-1000-8000-00805f9b34fb".split(" ")
		# second is faster but might not work on other headphones ig
		cmd = "gatttool -b 00:1B:66:C1:62:4F --char-read -a 0x2d".split(" ")
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
		try:
			p.wait(timeout = 1.5)
		except subprocess.TimeoutExpired:
			return None, None, "Timeout"
		assert p.poll() != None
		txt = p.stdout.read().strip().decode()
		error = p.stderr.read().strip().decode()
		value = None
		error_value = None
		if p.poll() != 0:
			error_value = int(error.split(" ")[-1][1:-1])
		else:
			try:
				value = int(txt.split(" ")[-1], 16)
			except ValueError:
				pass
		return value, error_value, error

	def get_status(self):
		if self.last_query_time + self.query_interval <= time.time():
			self.last_query_time = time.time()
			print("querying", file = sys.stderr)
			value, error_value, error = self.get_battery()
			self.last_error_value = error_value
			self.last_error = error
			if error_value != 16:
				self.last_value = value

		if self.last_value is not None:
			return {
				"full_text" : f"\uf025 {self.last_value}%",
				"color": self.COLOR,
			}
		elif self.last_error_value != 16:
			return {
				"full_text" : f"Error : {self.last_error}",
				"color": self.COLOR,
			}
		else:
			return None

if __name__ == "__main__":
	status = HeadphoneBatteryStatus()
	while True:
		pprint(status.get_status())
		time.sleep(0.5)
