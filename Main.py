import musicXML_scraper
import ChoiceLogic
import note_to_midi

def main(filename):
	with open(filename, 'r') as f:
		xml_string = "".join(i for i in f.readlines())

	chords, bpm = musicXML_scraper.getChords(xml_string)

	notes = []
	for chord in chords:
		notes += ChoiceLogic.choose_note(chord, notes)
	
	midi_file = note_to_midi.notes_to_midi(notes, bpm)

	return True
	


main('Blues For Alice.txt')