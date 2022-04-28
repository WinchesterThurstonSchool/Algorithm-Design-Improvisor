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
		self.logic()

	
	def make_chroma_weights(self):
		chroma_scale = self.chord.get_chromatic_tones()
		for i in chroma_scale:
			self.pitch_weights[i.pitch] = 1
			# adjust for lower octave as well
			self.pitch_weights[i.pitch-12] = 1
		return self.pitch_weights

	def make_chord_tone_weights(self):
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
			self.pitch_weights[j.pitch] = 3
			self.pitch_weights[j.pitch-12] = 3
		
		return self.pitch_weights

	def scale_tone_weights(self):
		scale_notes = self.chord.get_scale_notes()
			



	def logic(self):
		"""takes the information given and creates weighted pitches

		Returns:
			dict: dictionary of pitches and their weights
		"""
		self.make_chord_tone_weights()
		self.make_chroma_weights()
		# create cases based on the previous notes. 
		# Broad cases: Direction, Chromatic Resolution, interval

		past1 = self.past_notes[-1]
		past2 = self.past_notes[-2]

		# positive interval means upwards direction. negative means downwards
		interval = past1.pitch - past2.pitch

		# case 1: chromatic resolution. If the previous note is not within the bounds of the scale, resolve up or down by a half step

		if past1.pitch in self.chord.get_chromatic_tones():
			# really heavy weight on the chromatic steps
			self.pitch_weights[past1.pitch+1] = 10
			self.pitch_weights[past1.pitch-1] = 10

		# case 2: the direction of the previous notes is a scale going up by seconds
		if interval >0 and interval < 3:
			self.pitch_weights[past1.pitch+interval]=5

		elif interval < 0 and interval > -3:
			# WLOG, go down the scale 
			self.pitch_weights[past1.pitch-interval]=5
		
		else:
			# if these conditions arent met, look to the interval and weigh the colourful intervals
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
