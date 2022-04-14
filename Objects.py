# The timebase is an eigth note. This means that when the duration is 1, that means that the note lasts an eigth note.
TIMEBASE = 1/8

class Note:
	def __init__(self, pitch, duration = 1):
		# pitch is the nummber [0,88] of the note
		self.pitch = pitch
		self.duration = duration

class Chord:
	def __init__(self, notes, duration = 1):
		# notes is a list of Note objects
		self.notes = notes
		# default duration is the average duration of the notes
		self.duration = duration

def get_note_from_string(string):

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
	
