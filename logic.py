import Objects

TIMEBASE = Objects.TIMEBASE
### PARENT ORGANIZER CLASS ###
class Logic:
	def __init__(self, chord : Objects.Chord, past_notes = Objects.Note()):
		self.chord = chord
		# chromatic tones
		# scale tones
		# chord tones

### HERE GOES THE RHYTHM LOGIC ###

class Rhythm:
	def __init__(self, chord: Objects.Chord, past_notes = []):
		self.chord = chord
		self.weights = {"quarter": 1, "eighth": 1, "sixteenth": 1}
	
	# chromatic case
	#previous rhythm
	# weight dictionary
	# definite rhythms


### HERE GOES THE PITCH LOGIC ###

class Pitch:
	def __init__(self, rhythm : Rhythm):
		self.chord = rhythm.chord
		self.pastnotes = rhythm.past_notes
		self.rhythm = rhythm
		self.pitch_weights = {}

	def create_pitch_list(self):
		self.pitch_weights = {}
