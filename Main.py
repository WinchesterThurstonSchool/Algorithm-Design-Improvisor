import musicXML_scraper
import ChoiceLogic
import musicXML_scraper

def XMLtoImprov(filename):
	with open(filename, 'r') as f:
		xml_string = "".join(i for i in f.readlines())

	chords = musicXML_scraper.get_chords(xml_string)

	notes = []
	for chord in chords:
		notes.append(ChoiceLogic.choose_note(chord, notes))
	

	return notes



