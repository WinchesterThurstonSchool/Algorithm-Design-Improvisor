import Objects
from Objects import Chord, Note
TIMEBASE = Objects.TIMEBASE

### HERE GOES THE RHYTHM LOGIC ###


class Rhythm:
	def __init__(self, chord: Chord, past_notes=[]):
		self.chord = chord
		self.past_notes = past_notes

	# chromatic case
	#previous rhythm
	# weight dictionary
	# definite rhythms
