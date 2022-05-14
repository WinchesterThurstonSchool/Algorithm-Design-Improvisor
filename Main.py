import musicXML_scraper
import ChoiceLogic
import note_to_midi
import random

def main(filename, backtrack, bpm = 120):

	print("Opening File...")
	with open(filename, 'r') as f:
		xml_string = "".join(i for i in f.readlines())
	print("File Opened")

	print("Scraping MusicXML...")
	chords, bpm = musicXML_scraper.getChords(xml_string, bpm=bpm)
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

	note_to_midi.play_music(midi_file, backtrack)


	return True

def another_main_but_with_different_logic(filename, backtrack, bpm = 120):
	print("Opening File...")
	with open(filename, 'r') as f:
		xml_string = "".join(i for i in f.readlines())
	print("File Opened")

	print("Scraping MusicXML...")
	chords, bpm = musicXML_scraper.getChords(xml_string, bpm=bpm)
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

	note_to_midi.play_music(midi_file, backtrack)

# use main it sounds better
main("Oleo.xml", "Oleo.mp3", bpm=240)
