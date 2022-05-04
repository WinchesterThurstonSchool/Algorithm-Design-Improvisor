from matplotlib.colors import from_levels_and_colors
import Objects
from Objects import Chord, Note
TIMEBASE = Objects.TIMEBASE
from matplotlib import pyplot as plt
import random

### HERE GOES THE PITCH LOGIC ###

class Rhythm:
	def __init__(self, chord: Chord, past_notes=[]):
		self.chord = chord
		self.past_notes = past_notes

		self.rhythm_weights = {}
		

	# chromatic case

	def logic(self):
		if len(self.past_notes) < 2:
			self.rhythm_weights = {1/8:1}
			return self.rhythm_weights
		past1 = self.past_notes[-1]
		past2 = self.past_notes[-2]

		if past1.duration == 16:
			if past2.duration == 8:
				# the only option is a sixteenth note. Don't want 1/16 offsets
				self.rhythm_weights = {16: 1}
		elif past1.duration == 4:
			# heavy weight against long notes after a long note
			self.rhythm_weights = {
				2: 1,
				4: 1,
				8: 8,
				16: 2
			}
		elif past1.duration == 2:
			# equal weight for everything afer a half note except for another half note
			self.rhythm_weights = {
				4: 1,
				8: 1,
				16: 1
			}

		return self.rhythm_weights

	def dispaly(self):
		# visualize rhythm_wights
		x = list(self.rhythm_weights.keys())
		y = list(self.rhythm_weights.values())
		plt.bar(x, y)
		plt.show()

	def guess(self):
		self.logic()
		total_list = []
		for i in self.rhythm_weights:
			for j in range(self.rhythm_weights[i]):
				total_list.append(i)

		if len(total_list) > 0:
			return 1/random.choice(total_list)
		else:
			return 1/8
	

class GetPitch:
	def __init__(self, rhythm: Rhythm):
		self.chord = rhythm.chord
		self.past_notes = rhythm.past_notes
		self.rhythm = rhythm

		self.interval_weights = {}

		self.chroma_weight = 3
		self.ct_weight = 4
		self.color_ct_weight = 5
		self.scale_weight = 5

		self.pitch_weights = dict()


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

		# incase there aren't any past notes, make a random selection
		if len(self.past_notes) < 2:
			return {random.choice(list(self.pitch_weights.keys())):1}

		past1 = self.past_notes[-1]
		past2 = self.past_notes[-2]

		# positive interval means upwards direction. negative means downwards
		interval = past1.pitch - past2.pitch

		# case 1: chromatic resolution. If the previous note is not within the bounds of the scale, resolve up or down by a half step

		if past1.pitch in self.chord.get_chromatic_tones():
			# really heavy weight on the chromatic steps
			self.pitch_weights = {past1.pitch+1: 1, past1.pitch-1: 1}
			return self.pitch_weights

		# case 2: the direction of the previous notes is a scale going up by seconds
		if interval > 0 and interval < 3:
			self.pitch_weights[past1.pitch+interval] = 5

		elif interval < 0 and interval > -3:
			# WLOG, go down the scale
			self.pitch_weights[past1.pitch-interval] = 5

		else:
			# if these conditions arent met, we can consider some stuff later
			pass

		# distribute notes so that they're weighted well within a good range, not all 2 octaves
		for i in self.pitch_weights:
			if i < past1.pitch-6:
				self.pitch_weights[i] -= 3
			elif i > past1.pitch+6:
				self.pitch_weights[i] -= 3

		# if there's no usable notes, then just return a random note
		if set(self.pitch_weights.values()) == set([0]):
			self.pitch_weights[i-2] =2
			self.pitch_weights[i+2] = 2

		return self.pitch_weights
		# weight the dictionary based on cases
		# make list of notes based on the wegihts
		# randomly choose notes from the list

	def display(self):
		x = list(self.pitch_weights.keys())
		y = list(self.pitch_weights.values())
		plt.bar(x, y)
		plt.title(self.rhythm.past_notes[-1])
		plt.show()

	def guess(self):
		"""
			takes a dictionary of pitches and their weights and returns a note object based on randomness
		"""

		# make a list of the pitches for the number of times they have a weight
		self.pitch_weights = self.logic()
		pitches = []
		for i in self.pitch_weights:
			for j in range(self.pitch_weights[i]):
				pitches.append(i)

		# choose a random note from the list
		random_note_pitch = random.choice(pitches)

		# time to reverse engineer the pitch to a name
		notes = ["C", "C#/Db", "D", "D#/Eb", "E", "F",
                    "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
		note_name = notes[int(random_note_pitch) % 12]
		final_note = Note(note_name, random_note_pitch)
		return final_note


def choose_note(c: Chord, past_notes: list):
	"""
		takes a chord, two notes and returns a note based on the weights of the notes
	"""
	notes = []
	rhythm_sum = 0

	# add to notes for the total duration of the chord
	while rhythm_sum < c.duration:

		if len(past_notes)>2:
			past_notes = past_notes[-2:]

		r = Rhythm(c, past_notes)
		p = GetPitch(r)

		# our pitch and name storage
		note_pitch_name = p.guess()
		# rhythm storage
		rhythm = r.guess()

	# only want notes that are within the length of the chord
		notes.append(Note(note_pitch_name.name, note_pitch_name.pitch, duration = rhythm))
		rhythm_sum += rhythm

		# add the new note to the past notes
		past_notes += notes


	return notes

	

		
if __name__ == "__main__":
	C = Chord("D", "maj","min")
	n1 = Note("D", octave=4)
	n2 = Note("F#/Gb", octave=4)

	notes = choose_note(C, [n1, n2])
	print([i.name for i in notes])

