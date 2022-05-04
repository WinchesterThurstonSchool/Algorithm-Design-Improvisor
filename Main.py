import musicXML_scraper
import ChoiceLogic
import musicXML_scraper

def XMLtoImprov(filename):
	with open(filename, 'r') as f:
		xml_string = "".join(i for i in f.readlines())

	chords = musicXML_scraper.getChords(xml_string)

	notes = []
	for chord in chords:
		notes += ChoiceLogic.choose_note(chord, notes)
	

	return notes


notes = XMLtoImprov('Blues for Alice.txt')
print(notes)
