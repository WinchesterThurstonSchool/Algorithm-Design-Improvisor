import Objects
from Objects import Chord, Note
TIMEBASE = Objects.TIMEBASE

### HERE GOES THE RHYTHM LOGIC ###


class Rhythm:
	def __init__(self, chord: Chord, past_notes=[]):
		self.chord = chord
		self.past_notes = past_notes
		self.weights = {"quarter": 1, "eighth": 1, "sixteenth": 1}

	# chromatic case
	#previous rhythm
	# weight dictionary
	# definite rhythms
