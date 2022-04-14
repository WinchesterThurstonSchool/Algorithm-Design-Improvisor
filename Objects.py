class Note:
	def __init__(self, pitch: str, duration: float, octave: int, timebase=1/8):
		self.pitch = pitch
		self.duration = duration
		self.timebase = timebase
		self.octave = octave

	def __str__(self):
		return "Note: pitch: {}, duration: {}, octave: {}".format(self.pitch, self.duration, self.octave)


class Chord:
	def __init__(self, notes: list, timebase=1/8):
		self.notes = notes
		self.timebase = timebase
		# gets the length of the chord by average duration of the notes
		self.duration = sum([note.duration for note in notes])//len(notes)

	def set_duration(self, duration: float):
		self.duration = duration
