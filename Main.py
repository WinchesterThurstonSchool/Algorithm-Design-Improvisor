import musicXML_scraper
import ChoiceLogic
import note_to_midi
import random

def main(filename):

	print("Opening File...")
	with open(filename, 'r') as f:
		xml_string = "".join(i for i in f.readlines())
	print("File Opened")

	print("Scraping MusicXML...")
	chords, bpm = musicXML_scraper.getChords(xml_string)
	print("MusicXML Scraped")

	print("Generating Notes...")
	notes = []
	for chord in chords:
		notes += ChoiceLogic.choose_note(chord, notes)
	print("Notes Generated")

	print("Writing to MIDI...")
	midi_file = note_to_midi.convertToMidi(notes, bpm)
	print("MIDI Written")
	

	print(f"Finished! MIDI file saved as \"{midi_file}\"")

	note_to_midi.play_music(midi_file, "A Fine Romance.mp3")


	return True

def another_main_but_with_different_logic(filename):
	print("Opening File...")
	with open(filename, 'r') as f:
		xml_string = "".join(i for i in f.readlines())
	print("File Opened")

	print("Scraping MusicXML...")
	chords, bpm = musicXML_scraper.getChords(xml_string)
	print("MusicXML Scraped")

	print("Generating Notes...")
	notes = []
	for chord in chords:
		notes += ChoiceLogic.choose_multiple(chord, notes, random.randint(4, 16))
		
	print("Notes Generated")

	print("Writing to MIDI...")
	midi_file = note_to_midi.convertToMidi(notes, bpm)
	print("MIDI Written")

	print(f"Finished! MIDI file saved as \"{midi_file}\"")

	note_to_midi.play_music(midi_file, "A Fine Romance.mp3")

main("A Fine Romance.txt")