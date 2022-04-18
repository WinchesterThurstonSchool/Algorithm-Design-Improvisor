# The timebase is an eigth note. This means that when the duration is 1, that means that the note lasts an eigth note.
TIMEBASE = 1/8


# W = whole step, H = half step, A = augmented second
scales = {
	"major" : "WWHWWWH",
	"melodic minor" : "WHWWWHW",
	"harmonic minor" : "WHWHWAH",
	"dorian" : "WHWWWHW",
	"diminished 1" : "HWHWHWHW",
	"diminished 2" : "WHWHWHWH",
	"super lochrian" : "HWHWWWW",
	"mixolydian" : "WWHWWHW",
	"lydian" : "WWWHWWH" ,
	"half diminished" : "WHWHWWW"
}

class Note:
	def __init__(self, name: str, pitch = None, duration = 1):
		# pitch is the nummber [0,88] of the note
		self.name = name
		self.pitch = pitch
		self.duration = duration


	def __repr__(self):
		return str(self.pitch)

class Chord:
	def __init__(self, root: str, ctype : str, seven: str, extensions = [], duration = 1):
		"""This creates a chord type. Given a root note, a chord type, it will return a list of notes. 

		Args:
			root (str): The root note of the chord.
			ctype (str): type of the chord (major, minor, aug, dim, half_dim)
			seventh (str): type of 7 chord (maj, min) NOTE: no need for dom7: it's the same as maj w min 7
			extensions (list, optional): the tuple expression of the extensions. ex) (9,"#"), (11,""), (13,"b"). Defaults to [].
			duration (int, optional): the duration of the chord in default TIMEBASE. Defaults to 1.
		"""
		self.root = root
		self.ctype = ctype
		if ctype == "dim":
			self.seventh = "min"
		else:
			self.seven = seven
		self.extensions = extensions
		self.duration = duration

	def _get_scale(self):
		# minor just to test for now
		scale_list = []
		# determine the scales to use based on the chord

		# steps to determine scales:
		# 1. determine the ctype
		# 2. determine the 7th
		# 3. determine the extensions

		# no extensions necessary for maj/min seven chords
		if self.ctype == "m" or self.ctype == "-":
			if self.seven == "min":
					scale_list.append(scales["dorian"])
			elif self.seven == "maj":
				scale_list.append(scales["harmonic minor"])

		elif self.ctype == "M" or self.ctype == "maj":
			# here is the domonant seven case
			if self.seven == "min":
				if self.extensions == []:
					scale_list.append(scales["mixolydian"])
				else:
					if (9, "#") in self.extensions:
						scale_list.append(scales["super lochrian"])
					elif (9, "b") in self.extensions:
						scale_list.append(scales["diminished 1"])
					elif (11,"#") in self.extensions:
						scale_list.append(scales["lydian"])
			if self.seven == "maj":
				scale_list.append(scales["major"])

		elif self.ctype == "dim":
			# case for 7 already taken care of in __init__
			scale_list.append(scales["diminished 1"])
			scale_list.append(scales["diminished 2"])

		elif self.ctype == "aug":
			pass
		elif self.ctype == "sus":
			pass

		elif self.ctype == "half_dim":
			scale_list.append(scales["half diminished"])
		else:
			scale_list.append(scales["lydian"])

		return scale_list

	def get_notes(self):
		notes_list = ["C","C#/Db","D","D#/Eb","E","F","F#/Gb","G","G#/Ab","A","A#/Bb","B"]

		# this is the first of the determined scales we wanna check. LATER: we can make this more dynamic
		scale = self._get_scale()[0]
		indx = notes_list.index(self.root)
		notes = [Note(notes_list[indx])]
		
		for i in scale:
			if i == "H":
				# half step in the array
				indx += 1
			elif i == "W":
				# whole step in the array
				indx += 2
			elif i == "A":
				# augmented step in the array
				indx += 3
			else:
				raise Exception("Invalid interval")
			# don't overflow the array
			indx = indx % len(notes_list)
			notes.append(Note(notes_list[indx]))

		# all but the last because it's the root
		return notes[:-1]


print(Chord("G","maj","min", [(9,"#")]).get_notes())
