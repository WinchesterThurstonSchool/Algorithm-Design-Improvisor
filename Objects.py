import random
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
	"half diminished" : "WHWHWWW",
	"blues scale" : "AWHHAW"
}

class Note:
	def __init__(self, name: str, pitch = 64, octave = 4, duration = 1):
		"""Creates a note object.

		Args:
			name (str): [A,B,C,C# etc.]
			pitch (int, optional): The number of the pitch as it is in MIDI. Defaults to 64.
			octave (int, optional): The octave of the note ex.) A4, C6. Defaults to 4.
			duration (int, optional): The length of the note in timebase. Defaults to 1.
		"""
		self.name = name
		self.octave = octave
		self.pitch = self.get_pitch()
		self.duration = duration
	def get_pitch(self):
		notes = ["C","C#/Db","D","D#/Eb","E","F","F#/Gb","G","G#/Ab","A","A#/Bb","B"]
		return self.octave*8 + notes.index(self.name) + 28

	def __eq__(self, __o: str):
		return self.name == __o

	def __add__(self, __o: int):
		self.pitch += __o
		return self.pitch

	def __sub__(self, __o:int):
		self.pitch -= __o
		return self.pitch

	

	def __str__(self):
		return f"Pitch #: {self.get_pitch()}, {self.name}, {self.octave}, {self.duration}"

	def __repr__(self):
		return str(self.pitch)

	

class Chord:
	def __init__(self, root: str, ctype : str, seven: str, extensions = [], duration = 1):
		"""This creates a chord type. Given a root note, a chord type, it will return a list of notes. 

		Args:
			root (str): The root note of the chord.
			ctype (str): type of the chord (maj, min, aug, dim, half_dim)
			seventh (str): type of 7 chord (maj, min) NOTE: no need for dom7: it's the same as maj w min 7
			extensions (list, optional): the tuple expression of the extensions. ex) (9,"#"), (11,""), (13,"b"). Defaults to [].
			duration (int, optional): the duration of the chord in default TIMEBASE. Defaults to 1.
		"""
		self.root = root
		self.ctype = ctype
		if ctype == "dim":
			self.seven = "min"
		elif ctype == "aug":
			self.seven = "maj"
		elif ctype == "half_dim":
			self.seven = "min"
		else:
			self.seven = seven
		self.extensions = extensions
		self.duration = duration

	def get_chord_tones(self): 
		# currently ignores extensions because otherwise it's just a scale
		chord_tones = [Note(self.root)]
		notes_list = ["A","A#/Bb","B","C","C#/Db","D","D#/Eb","E","F","F#/Gb","G","G#/Ab"]
		chord_intervals = ""

		indx = notes_list.index(self.root)		
		# Steps to find chord tones:

		# determine maj,min,etc
		# determine 7

		if self.ctype == "maj" or self.ctype =="M":
			# base triad
			chord_intervals += "MM"
			if self.seven == "m" or self.seven == "min":
				chord_intervals += "m"
			elif self.seven == "M" or self.seven == "maj":
				chord_intervals += "M"

		elif self.ctype == "min" or self.ctype =="m":
			chord_intervals += "mM"
			if self.seven == "m" or self.seven == "min":
				chord_intervals += "m"
			elif self.seven == "M" or self.seven == "maj":
				chord_intervals += "M"
	
		elif self.ctype == "dim":
			chord_intervals += "mm"
			if self.seven == "m" or self.seven == "min":
				chord_intervals += "m"
			elif self.seven == "M" or self.seven == "maj":
				chord_intervals += "M"

		elif self.ctype == "aug":
			chord_intervals += "MM"
			if self.seven == "m" or self.seven == "min":
				chord_intervals += "m"
			elif self.seven == "M" or self.seven == "maj":
				chord_intervals += "M"
				
		elif self.ctype == "half_dim":
			chord_intervals += "mmM"

		for i in chord_intervals:
			if i == "M":
				indx += 4
			elif i == "m":
				indx += 3
			indx = indx % len(notes_list)
			chord_tones.append(Note(notes_list[indx]))

		return chord_tones

			
	
	def get_scales(self):
		# minor just to test for now
		scale_list = []
		# determine the scales to use based on the chord

		# steps to determine scales:
		# 1. determine the ctype
		# 2. determine the 7th
		# 3. determine the extensions

		# no extensions necessary for maj/min seven chords
		if self.ctype == "m" or self.ctype == "min":
			if self.seven == "min":
					scale_list.append(scales["dorian"])
			elif self.seven == "maj":
				scale_list.append(scales["harmonic minor"])
			else:
				scale_list.append(scales["melodic minor"])

		elif self.ctype == "M" or self.ctype == "maj":
			# here is the domonant seven case
			if self.seven == "min":
				if self.extensions == []:
					scale_list.append(scales["blues scale"])
					scale_list.append(scales["mixolydian"])
				else:
					if (9, "#") in self.extensions:
						scale_list.append(scales["super lochrian"])
					elif (9, "b") in self.extensions:
						scale_list.append(scales["diminished 1"])
					elif (11,"#") in self.extensions:
						scale_list.append(scales["lydian"])
					else:
						scale_list.append(scales["mixolydian"])
						
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
			scale_list.append(scales["major"])

		return scale_list

	def get_scale_notes(self):
		notes_list = ["C","C#/Db","D","D#/Eb","E","F","F#/Gb","G","G#/Ab","A","A#/Bb","B"]

		# this is the first of the determined scales we wanna check. LATER: we can make this more dynamic
		scale = self.get_scales()[random.randint(0,len(self.get_scales())-1)]
		indx = notes_list.index(self.root)
		notes = [Note(self.root).pitch]
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
			notes.append(Note(notes_list[indx]).pitch)
			notes.append(Note(notes_list[indx]).pitch-12)

		# all but the last because it's the root
		return notes[:-1]

	def get_chromatic_tones(self):
		"""creates a list of the chromatic notes in a chord

		Returns:
			list: a list of numerical pitches
		"""
		chroma_tones = []
		notes_list = ["C","C#/Db","D","D#/Eb","E","F","F#/Gb","G","G#/Ab","A","A#/Bb","B"]
		for i in notes_list:
			if Note(i).pitch not in self.get_scale_notes():
				chroma_tones.append(Note(i).pitch)
				chroma_tones.append(Note(i).pitch-12)

		return chroma_tones
	def __repr__(self):
		return str(self.root) + str(self.ctype) + str(self.seven) + str(self.extensions) + str(self.duration)


def chords_set():
	# testing combinations
	chords = []
	n = ["C","C#/Db","D","D#/Eb","E","F","F#/Gb","G","G#/Ab","A","A#/Bb","B"]
	tp = ["maj","min","dim","aug","half_dim"]
	ext = [9,11,13]
	a = ["#", "b", ""]
	s7 = ["maj","min"]

	for note in n:
		for typer in tp:
			for extension in ext:
				for accidental in a:
					for seven in s7:
						chords.append(Chord(note, typer, seven, [(extension, accidental)]))
	
	return chords