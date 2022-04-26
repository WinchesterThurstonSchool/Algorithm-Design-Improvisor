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

		self.interval_weights = {}

		self.pitch_weights = dict()
		self.create_pitch_list()
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
			self.pitch_weights[Note(notes_list[indx], octave=octave).pitch] = 0
			# keep the index looping through and not overflowing
			indx = (indx + 1) % len(notes_list)
			# up the octave every 12 and 24 notes
			if i==12 or i==24:
				octave += 1

		return self.pitch_weights
	
	def chroma_weights(self):
		chroma_scale = self.chord.get_chromatic_tones()
		for i in chroma_scale:
			self.pitch_weights[i.pitch] = 1
			# adjust for lower octave as well
			self.pitch_weights[i.pitch-12] = 1
		return self.pitch_weights

	def chord_tone_weights(self):
		chord_tones = self.chord.get_chord_tones()
		chroma_tones = self.chord.get_chromatic_tones()
		intersection = [i for i in chroma_tones if i in chord_tones]
		print(len(intersection))
		print(chord_tones, chroma_tones)
		# baseline chord tones
		for i in chord_tones:
			self.pitch_weights[i.pitch] = 1
			self.pitch_weights[i.pitch-12] = 1
		# weigh the colorful ones more
		for j in intersection:
			self.pitch_weights[j.pitch] = 4
			self.pitch_weights[j.pitch-12] = 4
		
		return self.pitch_weights
		



	def logic(self):
		"""takes the information given and creates weighted pitches

		Returns:
			dict: dictionary of pitches and their weights
		"""
		pitch_list = self.create_pitch_list()
		# create cases based on the previous notes. 
		# Broad cases: Direction, Chromatic Resolution, interval

		past1 = self.past_notes[-1]
		past2 = self.past_notes[-2]

		# positive interval means upwards direction. negative means downwards
		interval = past1.pitch - past2.pitch

		# case 1: chromatic resolution. If the previous note is not within the bounds of the scale, resolve up or down by a half step

		if past1.name in self.chord.get_chromatic_tones():
			pass

		# case 2: the direction of the previous notes is a scale going up by seconds
		if interval >0 and interval < 3:
			pass

		elif interval < 0 and interval > -3:
			# WLOG, go down the scale 
			pass
		
		else:
			# at all else, evenly distribute notes over chord tones
			pass

		return self.pitch_weights
		# weight the dictionary based on cases
		# make list of notes based on the wegihts
		# randomly choose notes from the list
	
	
		
		

C = Chord("C", "maj","min")
n1 = Note("D", octave=4)
n2 = Note("F", octave=4)
r = Rhythm(C, [n1, n2])
p = GetPitch(r)
p.chroma_weights()
p.chord_tone_weights()
print(p.pitch_weights)
