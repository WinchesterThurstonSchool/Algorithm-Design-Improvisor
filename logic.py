from matplotlib.colors import from_levels_and_colors
import Objects
from Objects import Chord, Note
TIMEBASE = Objects.TIMEBASE
from Rhythm import Rhythm
from matplotlib import pyplot as plt
import random

### HERE GOES THE PITCH LOGIC ###

class GetPitch:
	def __init__(self, rhythm : Rhythm):
		self.chord = rhythm.chord
		self.past_notes = rhythm.past_notes
		self.rhythm = rhythm

		self.interval_weights = {}

		self.chroma_weight = 2
		self.ct_weight = 4
		self.color_ct_weight =3
		self.scale_weight = 2

		self.pitch_weights = dict()
		self.logic()

	
	def make_chroma_weights(self):
		chroma_scale = self.chord.get_chromatic_tones()
		for i in chroma_scale:
			self.pitch_weights[i] = self.chroma_weight
			# adjust for lower octave as well
			self.pitch_weights[i-12] = self.chroma_weight
		return self.pitch_weights

	def make_chord_tone_weights(self):
		chord_tones = self.chord.get_chord_tones()
		chroma_tones = self.chord.get_chromatic_tones()
		intersection = [i for i in chroma_tones if i in chord_tones]
		# baseline chord tones
		for i in chord_tones:
			self.pitch_weights[i.pitch] = self.ct_weight
			self.pitch_weights[i.pitch-12] = self.ct_weight
		# weigh the colorful ones more
		for j in intersection:
			self.pitch_weights[j.pitch] = self.color_ct_weight
			self.pitch_weights[j.pitch-12] = self.color_ct_weight
		
		return self.pitch_weights

	def scale_tone_weights(self):
		scale_notes = self.chord.get_scale_notes()
		for i in scale_notes:
			self.pitch_weights[i] = self.scale_weight
			self.pitch_weights[i-12] = self.scale_weight

		# linear equation for deciding the weight of the scale tones

		return self.pitch_weights
			



	def logic(self):
		"""takes the information given and creates weighted pitches

		Returns:
			dict: dictionary of pitches and their weights
		"""
		self.make_chord_tone_weights()
		self.make_chroma_weights()
		self.scale_tone_weights()
		# create cases based on the previous notes. 
		# Broad cases: Direction, Chromatic Resolution, interval

		past1 = self.past_notes[-1]
		past2 = self.past_notes[-2]

		# positive interval means upwards direction. negative means downwards
		interval = past1.pitch - past2.pitch

		# case 1: chromatic resolution. If the previous note is not within the bounds of the scale, resolve up or down by a half step


		if past1.pitch in self.chord.get_chromatic_tones():
			# really heavy weight on the chromatic steps
			self.pitch_weights = {past1.pitch+1:1, past1.pitch-1:1}
			return self.pitch_weights

		# case 2: the direction of the previous notes is a scale going up by seconds
		if interval >0 and interval < 3:
			self.pitch_weights[past1.pitch+interval]=5

		elif interval < 0 and interval > -3:
			# WLOG, go down the scale 
			self.pitch_weights[past1.pitch-interval]=5
		
		else:
			# if these conditions arent met, we can consider some stuff later
			pass


		# distribute notes so that they're weighted well within a good range, not all 2 octaves
		for i in self.pitch_weights:
			if i<past1.pitch-6:
				self.pitch_weights[i] -= 2
			elif i>past1.pitch+6:
				self.pitch_weights[i] -= 2

		
		return self.pitch_weights
		# weight the dictionary based on cases
		# make list of notes based on the wegihts
		# randomly choose notes from the list

	def display(self):
		x = list(self.pitch_weights.keys())
		y = list(self.pitch_weights.values())
		plt.bar(x,y)
		plt.title(self.rhythm.past_notes[-1])
		plt.show()
	

	def guess(self):
		"""
			takes a dictionary of pitches and their weights and returns a note object based on randomness
		"""

		# make a list of the pitches for the number of times they have a weight
		pitches = []
		for i in self.pitch_weights:
			for j in range(self.pitch_weights[i]):
				pitches.append(i)

		# choose a random note from the list
		r = random.randint(0, len(pitches)-1)
		random_note_pitch = pitches[r]


		# time to reverse engineer the pitch to a name
		notes = ["C", "C#/Db", "D", "D#/Eb", "E", "F",
                    "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
		note_name = notes[random_note_pitch % 12]
		final_note = Note(note_name, random_note_pitch)
		return final_note

	

	
		
		

C = Chord("D", "maj","min")
n1 = Note("C", octave=4)
n2 = Note("D", octave=4)
r = Rhythm(C, [n1, n2])
p = GetPitch(r)

for i in range(30):
	n2 = n1
	n1 = p.guess()
	r = Rhythm(C, [n1, n2])
	p = GetPitch(r)
	p.display()
	print(n1)

