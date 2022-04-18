# The timebase is an eigth note. This means that when the duration is 1, that means that the note lasts an eigth note.
TIMEBASE = 1/8

scales = {
	"major" : "WWHWWWH",
	"melodic minor" : "WHWWWHW",
	"dorian" : "WHWWWHW"
}

class Note:
	def __init__(self, pitch, duration = 1):
		# pitch is the nummber [0,88] of the note
		self.pitch = pitch
		self.duration = duration

class Chord:
	def __init__(self, root, ctype, seventh, extensions = [], duration = 1):
		"""This creates a chord type. Given a root note, a chord type, and a fifth, it will return a list of notes. 

		Args:
			root (str): The root note of the chord.
			ctype (str): type of the chord (major, minor, aug, dim)
			seventh (str): type of 7 chord (maj, min, 7)
			extensions (list, optional): the tuple expression of the extensions. ex) (9,"#"), (11,""), (13,"b"). Defaults to [].
			duration (int, optional): the duration of the chord in default TIMEBASE. Defaults to 1.
		"""
		self.root = root
		self.ctype = ctype
		self.seventh = seventh
		self.extensions = extensions
		self.duration = duration

	def _get_scale(self):
		# minor just to test for now
		scale = []
		# determine the scales to use based on the chord

		# steps to determine scales:
		# 1. determine the ctype
		# 2. determine the 7th
		# 3. determine the extensions
		if self.ctype == "m" or self.ctype == "-":
			pass
		elif self.ctype == "M" or self.ctype == "maj":
			pass
		elif self.ctype == "dim":
			pass
		elif self.ctype == "aug":
			pass 
		elif self.ctype == "sus":
			pass
		else:
			pass

		return scale

	def get_notes(self):
		notes_list = ["C","C#/Db","D","D#/Eb","E","F","F#/Gb","G","G#/Ab","A","A#/Bb","B"]

		# this is the first of the determined scales we wanna check. LATER: we can make this more dynamic
		scale = self._get_scale()[0]
		indx = notes_list.index(self.root)
		notes = [notes_list[indx]]
		
		for i in scale:
			if i == "H":
				# half step in the array
				indx += 1
			elif i == "W":
				# whole step in the array
				indx += 2
			else:
				raise Exception("Invalid interval")
			# don't overflow the array
			indx = indx % len(notes_list)
			notes.append(notes_list[indx])

		return notes




def number_from_note(string):

	note = 1
	list_of_notes = ["A", "A#", "B", "C", "C#",
                  "D", "D#", "E", "F", "F#", "G", "G#"]

	# clean our input string so that we can use enharmonic tones
	if string == "Bb":
		string = "A#"
	elif string == "Cb":
		string = "B"
	elif string == "Db":
		string = "C#"
	elif string == "Eb":
		string = "D#"
	elif string == "Fb":
		string = "E"
	elif string == "Gb":
		string = "F#"
	elif string == "Ab":
		string = "G#"
	
	# seperate the octave from the note
	base = string[:-1]
	octave = string[-1]
	
	note = octave*8 + list_of_notes.index(base)

	return note
	

print(Chord("G","maj",1,1,[(9,1)]).get_notes())
