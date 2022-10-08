import libvirt

class VMStatus:
	COLOR_RED = "#881111ff"
	COLOR_GREEN = "#118811ff"
	def __init__(self):
		self.conn = None
		self.win10 = None
	def get_status(self):
		if self.conn == None:
			try:
				self.conn = libvirt.open("qemu:///system")
			except libvirt.libvirtError as e:
				return None
		if self.win10 == None:
			for domain in self.conn.listAllDomains():
				if domain.name() == "win10":
					self.win10 = domain
					break
			else:
				return None
		if not self.win10.isActive():
			return None
		is_keyboard_connected = self.win10.XMLDesc().find("0x258a") != -1
		is_mouse_connected = self.win10.XMLDesc().find("0x1b1c") != -1
		ret = []
		text_skeleton = "{} owns {}"
		color_arr = [self.COLOR_GREEN, self.COLOR_RED]
		owner_arr = ["PC", "WM"]
		return [
				{"full_text" : text_skeleton.format(owner_arr[is_keyboard_connected], "keyboard"),
					"color" : color_arr[is_keyboard_connected]}, 
				{"full_text" : text_skeleton.format(owner_arr[is_mouse_connected], "mouse"),
					"color" : color_arr[is_mouse_connected]}, 
		]

