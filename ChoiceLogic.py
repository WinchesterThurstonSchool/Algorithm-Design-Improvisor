import Objects
from Objects import Chord, Note
TIMEBASE = Objects.TIMEBASE
from matplotlib import pyplot as plt
import random

### HERE GOES THE PITCH LOGIC ###

def toName(pitch):
	notes = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
	return notes[pitch%12]


class Rhythm:
	def __init__(self, chord: Chord, past_notes=[]):
		self.chord = chord
		self.past_notes = past_notes

		self.rhythm_weights = dict()
		

	# chromatic case

	def logic(self):
		if len(self.past_notes) < 2:
			self.rhythm_weights = {1/8:1}
			return self.rhythm_weights
		
		past1 = self.past_notes[-1]
		past2 = self.past_notes[-2]

		if past1.duration == 1/16:
			if past2.duration == 1/8:
				# the only option is a sixteenth note. Don't want 1/16 offsets
				self.rhythm_weights = {1/16: 1}
			elif past2.duration == 1/16:
				self.rhythm_weights = {1/8: 1}
		elif past1.duration == 1/4:
			# heavy weight against long notes after a long note
			self.rhythm_weights = {
				1/2: 1,
				1/4: 4,
				1/8: 40,
				1/16: 1
			}
		elif past1.duration == 1/2:
			# equal weight for everything afer a half note except for another half note
			self.rhythm_weights = {
				1/4: 10,
				1/8: 40,
				1/16: 1
			}
		elif past1.duration == 1/8:
			self.rhythm_weights = {
				1/2: 1,
				1/4: 3,
				1/8 :30,
				1/16: 1
			}
		return self.rhythm_weights

	def display(self):
		# visualize rhythm_wights
		x = list(self.rhythm_weights.keys())
		y = list(self.rhythm_weights.values())
		plt.bar(x, y)
		plt.show()

	def guess(self):
		self.rhythm_weights = self.logic()
		total_list = []
		for i in self.rhythm_weights:
			for j in range(self.rhythm_weights[i]):
				total_list.append(i)

		if len(total_list) > 0:
			return random.choice(total_list)
		else:
			return 1/8
	

class GetPitch:
	def __init__(self, rhythm: Rhythm):
		self.chord = rhythm.chord
		self.past_notes = rhythm.past_notes
		self.rhythm = rhythm

		self.interval_weights = {}

		self.chroma_weight = 1
		self.ct_weight = 5
		self.color_ct_weight = 2
		self.scale_weight = 10

		self.pitch_weights = dict()

	def get_weights(self):
		return [self.chroma_weight, self.ct_weight, self.color_ct_weight, self.scale_weight]

	def set_weights(self, weights):
		self.chroma_weight = weights[0]
		self.ct_weight = weights[1]
		self.color_ct_weight = weights[2]
		self.scale_weight = weights[3]


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
			self.pitch_weights[i] = self.ct_weight
			self.pitch_weights[i-12] = self.ct_weight
		# weigh the colorful ones more
		for j in intersection:
			self.pitch_weights[j] = self.color_ct_weight
			self.pitch_weights[j-12] = self.color_ct_weight

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
		self.pitch_weights[past1.pitch] = 5

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
			self.pitch_weights[past1.pitch-interval] =  5


		# distribute notes so that they're weighted well within a good range, not all 2 octaves
		slope = self.pitch_weights[past1.pitch] / (past1.pitch- min(self.pitch_weights)) / 2
		for i in self.pitch_weights:
			self.pitch_weights[i] = abs(int(-slope *1/2* abs(i - past1.pitch) + self.pitch_weights[i]))
		

		# if there's no usable notes, then just return a random note
		if set(self.pitch_weights.values()) == set([0]):
			self.pitch_weights = {0:1}

		self.pitch_weights[past1.pitch] = 0

		return self.pitch_weights
		# weight the dictionary based on cases
		# make list of notes based on the wegihts
		# randomly choose notes from the list

	def normal_weigh(self, listy, past_note):
		slope = listy[past_note] / (past_note- min(listy))
		for i in listy:
			listy[i] = abs(int(-slope * abs(i - past_note) + listy[i]))
		return listy

	def logic2(self):
		# determines the outlier of a scale
		accidental_threshold = .95
		# probability that the next note chosen is based on the sacle
		scale_threshold = 0.8
		# OUTLINE:
		# Get a few past notes (like 4)
		# go up/down the scale, adding osme chromaticism sometimes
		# if not going up or down the scale, hit some chord tones

		# choose some random notes if there aren't enough starting notes
		#! fix starting notes later
		past_notes = self.past_notes[-2:]
		if len(past_notes) < 2:
			past_notes = [random.randint(50,70), random.randint(50,70)]
		for i in range(len(past_notes)):
			if not isinstance(past_notes[i], int):
				past_notes[i] = past_notes[i].pitch
		
		# get the list of ontes
		chord_tones = sorted(self.chord.get_chord_tones())
		scale_tones =sorted(self.chord.get_scale_notes())
		chroma_tones = sorted(self.chord.get_chromatic_tones())
		pattern_probability = random.random()

		# chromatic resolution comes first
		if past_notes[-1] in chroma_tones:
			print("resolving chromatic")
			self.pitch_weights = {past_notes[-1]+1:1, past_notes[-1]-1:1}
			
		# sacle decision time
		elif pattern_probability < scale_threshold:
			if past_notes[-1] in scale_tones:
				print("scale decision")
				current_index = scale_tones.index(past_notes[-1])
				r = random.random()
				# next scale tone up or down
				if r < accidental_threshold:
					if past_notes[-1] - past_notes[-2] > 0:
						local_scale_weight_up = self.scale_weight * 4
						local_scale_weight_down = self.scale_weight
					else:
						local_scale_weight_down = self.scale_weight * 4
						local_scale_weight_up = self.scale_weight
					self.pitch_weights = {scale_tones[current_index+1]:local_scale_weight_up, scale_tones[current_index-1]:local_scale_weight_down}
				# chromatic tone
				else:
					self.pitch_weights = {scale_tones[current_index+1]-1:self.chroma_weight, scale_tones[current_index-1]+1:self.chroma_weight}
			else:
				self.pitch_weights = {random.choice(scale_tones):1}
		# chord tone decision time
		elif pattern_probability >= scale_threshold:
			note = random.choice(chord_tones)
			self.pitch_weights = {note.pitch: self.ct_weight}

		
		
		return self.pitch_weights



	def display(self):
		notes = ["C", "C#/Db", "D", "D#/Eb", "E", "F",
                    "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
		x = [notes[i%12] for i in self.pitch_weights.keys()]
		y = list(self.pitch_weights.values())
		plt.bar(x, y)
		plt.title(self.past_notes[-1])
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
		# don't want leaps too big
		# if len(self.past_notes) > 0:
		# 	if random_note_pitch - self.past_notes[-1].pitch > 5:
		# 		random_note_pitch = self.past_notes[-1].pitch + 2
		# 		print("interval manipulated")
		# time to reverse engineer the pitch to a name
		notes = ["C", "C#/Db", "D", "D#/Eb", "E", "F",
                    "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
		note_name = notes[int(random_note_pitch) % 12]
		final_note = Note(note_name, random_note_pitch)
		return final_note

	def guess_several(self, num_guesses):
		try:
			scale_tones = sorted(self.chord.get_scale_notes())
			chord_tones = sorted(self.chord.get_chord_tones())
			if len(self.past_notes) < 1:
				past1 = random.randint(50, 70)
			else:
				if not isinstance(self.past_notes[-1], int):
					past1 = self.past_notes[-1].pitch
				else:
					past1 = self.past_notes[-1]

			if past1 not in scale_tones:
				print("not in scale, modifying")
				past1 = random.choice(scale_tones)
			elif past1 not in chord_tones:
				print("not in chord, modifying")
				past1 = random.choice(chord_tones)

			random_direction = random.random()
			scale_or_chord = random.random()
			if random_direction < 0.5:
				print("Going up")
				# go up
				if scale_or_chord < 0.5:
					print("choosing scale")
					# scale
					index = scale_tones.index(past1)
					try:
						return scale_tones[index+1:index+num_guesses+1]
					except:
						print("out of range, reutrning rest of scale")
						return scale_tones[index+1:]
				else:
					print("chosoing chord")
					# chord
					index = chord_tones.index(past1)
					try:
						return chord_tones[index+1:index+num_guesses+1]
					except:
						print("out of range, reutrning rest of chord")
						return chord_tones[index+1:]

			else:
				print("going down")
				# go down
				if scale_or_chord < 0.5:
					print("choosing scale")
					# scale
					index = scale_tones.index(past1)
					try:
						return scale_tones[index:index-num_guesses-1:-1]
					except:
						print("out of range, reutrning rest of scale")
						return scale_tones[:index-1]
				else:
					# chord
					print("Choosing chord")
					index = chord_tones.index(past1)
					try:
						return chord_tones[index:index-num_guesses-1:-1]
					except:
						print("out of range, reutrning rest of chord")
						return chord_tones[:index-1]
		except:
			print("something went wrong :( returning a different logic")
			return [random.randint(60,80)]


def choose_note(c: Chord, past_notes: list, custom_weights = []):
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
		if custom_weights != []:
			p.set_weights(custom_weights)

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

def choose_multiple(c: Chord, past_notes: list, num_guesses: int, custom_weights = []):
	rhythm = []
	notes = []
	rhythm_sum = 0

	while rhythm_sum < c.duration:

		if len(past_notes)>2:
			past_notes = past_notes[-2:]

		
		
		r = Rhythm(c, past_notes)
		p = GetPitch(r)

		if custom_weights != []:
			p.set_weights(custom_weights)
		
		# our pitch storage
		# using splicing because it could be more than that many
		note_pitch_name = p.guess_several(num_guesses)[:num_guesses]
		# rhythm storage
		for i in range(num_guesses):
			rhythm.append(r.guess())

		# making them the same length
		rhythm = rhythm[:len(note_pitch_name)]

		for i in range(len(note_pitch_name)):
			if rhythm_sum < c.duration:

				notes.append(Note(toName(note_pitch_name[i]), note_pitch_name[i], rhythm[i]))
			rhythm_sum += rhythm[i]


		past_notes += notes
	# this returns integers
	return notes
		
if __name__ == "__main__":
	C = Chord("C", "maj","min")
	n1 = Note("D", octave=4)
	n2 = Note("E", octave=4)

	notes = choose_multiple(C, [n1, n2], 8)
	print(notes)

