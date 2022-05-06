import musicXML_scraper
import ChoiceLogic
import note_to_midi

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

	return True




main('A Fine Romance.txt')