from datetime import timedelta

def format_timedelta(t):
	ms = None
	if isinstance(t, timedelta):
		ms = t.microseconds
		ms -= (ms % int(1e5))
		t = t.total_seconds()
	if isinstance(t, float):
		t = int(t)

	assert isinstance(t, int)
	#time_str = ""
	ret = f"{(t // 60) % 60:02}:{(t) % 60:02}"
	if t >= 60 * 60:
		ret = f"{(t // (60 * 60)) % 60:02}:{ret}"
	if ms != None:
		ret = f"{ret}:{ms // 1000:03}"
	return ret
	return time_str
