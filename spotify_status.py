import dbus
import time
from status import Status
from misc import format_timedelta
from pprint import pprint

class SpotifyStatus(Status):
	play_utf=""
	play_utf = "\uf04b"
	pause_utf=""
	#play_utf="P"
	#pause_utf="p"
	last_song = None
	last_song_playback_status = False
	last_song_playing_time = 0.0
	last_update_time = time.time()
	invalid_flag = True

	@staticmethod
	def get_spotify_status():
		session_bus = dbus.SessionBus()
		spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
											 "/org/mpris/MediaPlayer2")
		spotify_properties = dbus.Interface(spotify_bus,
											"org.freedesktop.DBus.Properties")
		metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
		playback_status = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "PlaybackStatus")
		return metadata, playback_status

	def get_status(self):
		try:
			metadata, playback_status = self.get_spotify_status()
		except dbus.exceptions.DBusException:
			return None
		song_length = metadata["mpris:length"] / 1e6
		song_length_str = format_timedelta(song_length)
		song_artist = ", ".join(metadata["xesam:artist"])
		song_title = metadata["xesam:title"]
		curr_song = (song_title, song_artist, song_length)
		curr_t = time.time()
		if self.last_song != curr_song:
			self.invalid_flag = self.last_song == None
			self.last_song = curr_song
			self.last_song_playing_time = 0.0
		else:
			if self.last_song_playback_status == "Playing":
				self.last_song_playing_time += curr_t - self.last_update_time

		while song_length > 1 and self.last_song_playing_time > song_length+1:
			self.last_song_playing_time -= song_length
		self.last_song_playback_status = playback_status
		self.last_update_time = curr_t
		song_playing_time_str = "" if self.invalid_flag else f"{format_timedelta(self.last_song_playing_time)}/"
		song_playing_str = self.play_utf if playback_status == "Playing" else self.pause_utf
		return {
			"full_text" : f"{song_playing_str} {song_artist} - {song_title} ({song_playing_time_str}{song_length_str})",
			"color": self.COLOR
		}



