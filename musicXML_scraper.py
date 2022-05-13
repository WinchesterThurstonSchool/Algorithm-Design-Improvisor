from Objects import Chord, Note
#things I need
#parse the 'kind' line to see if its a major or minor or whatever
#in the 'pitch' object get the step(letter) and alter(number, convert to flats or sharps)
#degree value and degree alter (check notes and talk to Marco about how to write)
#element index website: https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/
bfa = open("Blues For Alice.txt", "r")
bfaString = "".join(i for i in bfa.readlines())

def find_bpm(ms, num_beats):
    return 60000/ms * num_beats

def writeChord(t, bpm = 168):
    kind = ''
    degreeValue = ''
    degreeAlter = ''
    noteLetter = ''
    noteAlter = ''
    note = ''
    ctype = ''
    seven = ''
    degree = []
    duration = 0

    kindNum = 12
    if "<kind text=" in t:
        kind = t[t.index('<kind text="') + kindNum]
        #gotta do the major major minor minor stuff so not 7
        while kind[len(kind) -1] != '7':
            kindNum += 1
            kind = kind + t[t.index('<kind text="') + kindNum]
    elif "<kind use-symbols=" in t:
        kind = ""
        ctype = "dim"

    if "<degree-value>" in t:
        degreeValue = t[t.index('<degree-value>') + 14]
        degreeAlter = t[t.index('<degree-alter>') + 14]
        if degreeAlter == '-':
            degreeAlter = degreeAlter + t[t.index('<degree-alter>') + 15]
        degreeTypeIndex = t.index('<degree-alter>') + 1
    else:
        degreeValue, degreeAlter = None, None

    noteLetter = t[t.index('<root-step>') + 11] 
    noteAlter = t[t.index('<root-alter>') + 12]

    durationNum = 10
    duration = t[t.index('<duration>') + durationNum]
    while duration[len(duration)-1] != '<':
        durationNum += 1
        duration = duration + t[t.index('<duration>') + durationNum]

    # because the < is included
    duration = duration[:-1]

    if noteAlter == '-':
        noteAlter = 'b'
    elif noteAlter == '1':
        noteAlter = '#'
    elif noteAlter == "0":
        noteAlter = ''

    if degreeAlter == '-1':
        degreeAlter = 'b'
    elif degreeAlter == '1':
        degreeAlter = '#'

    note = noteLetter + noteAlter
    if note == 'A#' or note == 'Bb':
        note = 'A#/Bb'
    elif note == 'C#' or note == 'Db':
        note = 'C#/Db'
    elif note == 'F#' or note == 'Gb':
        note = 'F#/Gb'
    elif note == 'G#' or note == 'Ab':
        note = 'G#/Ab'
    elif note == "D#" or note == "Eb":
        note = "D#/Eb"


    if kind == 'maj7':
        ctype = 'maj'
        seven = 'maj'
    elif kind == 'm7':
        ctype = 'min'
        seven = 'min'
    elif kind == '7':
        ctype = 'maj'
        seven = 'min'
    
    if degreeAlter is None or degreeValue is None:
        degree = []
    else:
        degree = [int(degreeValue), degreeAlter]

    if degree == [5, 'b']:
        ctype = "half_dim"
        degree = []

    # normalize duration to bpm
    single_beat_in_ms = 60000/bpm
    # idk what I did wrong but for some reason it has to be divided by 2 in order to be the correct duration
    duration = int(int(duration) / single_beat_in_ms / 2)

    #gotta put the degree stuff in a tuple

    fullChord = Chord(note, ctype, seven, degree, duration)
    return fullChord

# take the bfa string and split it up into chunks of chords
def getChords(string, bpm = 160):
    chunks  = string.split("<harmony")
    chords = []
    # from teh second chunk because the first one is just the header
    for chunk in chunks[1:]:
        chords.append(writeChord(chunk, bpm))
    
    return chords, bpm

if __name__ == "__main__":
    print(getChords(bfaString))
#print(bfaString)
