import Objects
from Objects import Chord, Note
TIMEBASE = Objects.TIMEBASE

### HERE GOES THE RHYTHM LOGIC ###

class Rhythm:
	def __init__(self, chord: Chord, past_notes = []):
		self.chord = chord
		self.past_notes = past_notes
		self.weights = {"quarter": 1, "eighth": 1, "sixteenth": 1}
	
	# chromatic case
	#previous rhythm
	# weight dictionary
	# definite rhythms


### HERE GOES THE PITCH LOGIC ###

class Pitch:
	def __init__(self, rhythm : Rhythm):
		self.chord = rhythm.chord
		self.past_notes = rhythm.past_notes
		self.rhythm = rhythm
		self.pitch_weights = {}


	def create_pitch_list(self):
		self.pitch_weights = {}
		# determining what octave of the scale to center around. -1 because we go up two octaves later
		octave = self.past_notes[-1].octave -1
		notes_list = ["A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]
		# the location of the root of the chord in the notes list
		indx = notes_list.index(self.chord.root)
		# 26 because we want a full 2 octaves inclusive
		for i in range(1,26):
			# add that note to the list
			self.pitch_weights[Note(notes_list[indx], octave=octave)] = 1
			# keep the index looping through and not overflowing
			indx = (indx + 1) % len(notes_list)
			# up the octave every 12 and 24 notes
			if i==12 or i==24:
				octave += 1
		


r = Rhythm(Chord("C", "maj", "M", extensions =[(9,'b')]), past_notes=[Note("C", octave=4)])
p = Pitch(r)
p.create_pitch_list()
print(p.pitch_weights)
		
