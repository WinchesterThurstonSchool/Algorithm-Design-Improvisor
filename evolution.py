"""
THIS IS NO LONGER NEEDED. UNNECESSARY CODE. GOOD FOR PROJECT REFERENCE THOUGH
"""
import ChoiceLogic
import random
import musicXML_scraper
import note_to_midi
import json
import Objects
from Objects import Note

class Brain:
	def __init__(self):
		self.weights = []
		self.step = 0
		# size is the number of weights we're working with
		self.size = 6
		self.randomize()

	def randomize(self):
		for i in range(self.size):
			self.weights.append(random.randint(0,50))
	
	def clone(self):
		return self

	def mutate(self):
		mutation_rate = .4
		for i in range(self.size):
			rand = random.random()
			if rand < mutation_rate:
				self.weights[i] = random.randint(0,50)


class Individual:
	def __init__(self, chord: Objects.Chord, past_notes: list[Objects.Note], goal: list):
		# there are 6 weights to be adjusted. DO NOT CHANGE THIS 
		self.brain = Brain()
		self.weight = self.brain.weights
		self.guess = ChoiceLogic.GetPitch(ChoiceLogic.Rhythm(
			chord, past_notes))
		self.guess.set_weights(self.weight)
		self.guess = self.guess.guess()
		self.goal = goal
		self.fitness = 0.0
		self.is_best = False
		self.dead = False
		self.num_chords = 1
		self.goal = 0
		self.filename = "A Fine Romance.txt"

	def show(self):
		if self.is_best:
			print(f"Best individual: {self.weight}")
		else:
			print(f"Current Individual: {self.weight}")

	def reached_goal(self):
		return self.goal == self.guess

	def calculate_fitness(self):
		if self.reached_goal():
			self.fitness = 1
		else:
			for i in range(len(self.guess)):
				self.fitness = 1 / (self.guess[i] - self.goal[i])
		

	def gimme_baby(self):
		baby = self
		baby.brain = self.brain.clone()
		return baby
	
	def __str__(self):
		return f"{self.weight}"
	def __repr__(self):
		return f"{self.weight}"

class Population:
	def __init__(self, chord, past_notes, goal, size = 50):

		self.individuals = []
		with open('notes_weights.json', 'r') as f:
			try:
				json_ls = json.load(f)
			except:
				json_ls = []
			if len(json_ls) > 0 :
				for i in range(0,size):
					indiv = Individual(chord, past_notes, goal)
					indiv.wight = json_ls[str(i)]
					self.individuals.append(indiv)
			else:
				print("No Data Found. Making new weights")
				for i in range(size):
					indiv = Individual(chord, past_notes, goal)
					self.individuals.append(indiv)


		self.gen = 0
		self.best_indiv = None
		self.is_best = False
		self.fitness_sum = 0

	def show(self):
		print(f"Best Individual: {self.individuals[self.best_indiv]}")
		self.individuals[0] = self.individuals[self.best_indiv]
		json_dict = dict(zip(range(len(self.individuals)),[i.weight for i in self.individuals]))
		with open("notes_weights.json", "w") as f:
			json.dump(json_dict, f, sort_keys=True, indent=4)
			print("Json Dumped :D")

		print(f"Generation: {self.gen}")
		
	
	def calculate_fitness(self):
		for i in self.individuals:
			i.calculate_fitness()
	
	def calculate_fitness_sum(self):
		for i in self.individuals:
			self.fitness_sum += i.fitness

	def natural_selection(self):
		new_individuals = [i for i in self.individuals]
		self.calculate_fitness_sum()
		self.set_best_dot()
		new_individuals[0] = self.individuals[self.best_indiv].gimme_baby()
		new_individuals[0].is_best = True

		for i in range(1, len(new_individuals)):
			parent = self.selectParent()
			new_individuals[i] = parent.gimme_baby()
		self.individuals = new_individuals
		self.gen += 1

	def selectParent(self):
		rand = random.uniform(0.0, self.fitness_sum)
		running_sum = 0
		for i in self.individuals:
			running_sum += i.fitness
			if running_sum > rand:
				return i
		return self.individuals[0]

	def mutate_babies(self):
		for i in self.individuals[1:]:
			i.brain.mutate()

	def set_best_dot(self):
		maximum = 0
		max_index = 0
		for i in range(len(self.individuals)):
			if self.individuals[i].fitness > maximum:
				maximum = self.individuals[i].fitness
				max_index = i
			self.best_indiv = max_index


def main():
	test = Population(7, Objects.Chord("C", "maj", "min"), [Note("C"), Note(
		"D"), Note("D#/Eb"), Note("E"), Note("G"), Note("A#/Bb"), Note("F#/Gb"), Note("G")])

	while True:
		test.calculate_fitness()
		test.natural_selection()
		test.mutate_babies()
		test.show()
main()
