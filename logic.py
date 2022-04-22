import Objects
from Objects import Chord, Note
TIMEBASE = Objects.TIMEBASE
from Rhythm import Rhythm

### HERE GOES THE PITCH LOGIC ###

class GetPitch:
	def __init__(self, rhythm : Rhythm):
		self.chord = rhythm.chord
		self.past_notes = rhythm.past_notes
		self.rhythm = rhythm
		self.pitch_weights = {}
		self.logic()


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

	def logic(self):
		pitch_list = self.create_pitch_list()
		# create cases based on the previous notes. 
		# Broad cases: Direction, Chromatic Resolution, interval

		past1 = self.past_notes[-1]
		past2 = self.past_notes[-2]

		# case 1: chromatic resolution. If the previous note is not within the bounds of the scale, resolve up or down by a half step

		if past1 not in self.chord.get_scale_notes():
			# Note: when adding to a note type, it adds to the pitch itself
			# 60-40 up to down resolution
			self.pitch_weights[past1+1] = 0.6
			self.pitch_weights[past1-1] = 0.4

		# weight the dictionary based on cases
		# make list of notes based on the wegihts
		# randomly choose notes from the list
	
	
		
		


r = Rhythm(Chord("C", "maj", "M", extensions =[(9,'b')]), past_notes=[Note("C", octave=4), Note("C#/Db", octave=4)])
p = GetPitch(r)
p.create_pitch_list()
print(p.pitch_weights)
