from status import Status
from datetime import datetime
class TimeStatus(Status):
	def get_status(self):
		return {
			"full_text" : datetime.now().strftime("%b, %A %Y-%m-%d %H:%M:%S "),
			"color": self.COLOR,
		}

