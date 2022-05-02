from Objects import Chord, Note
#things I need
#parse the 'kind' line to see if its a major or minor or whatever
#in the 'pitch' object get the step(letter) and alter(number, convert to flats or sharps)
#degree value and degree alter (check notes and talk to Marco about how to write)
#element index website: https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/
bfa = open("Blues For Alice.txt", "r")
bfaString = "".join(i for i in bfa.readlines())

def writeChord(string):
    t = string
    i = 0
    end_chunk = t.index("</harmony>")
    while i < end_chunk:
        i += 1
        if  "<!-" in t[i:i+3]:
            t = t[i:]
        

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
        kind = t[t.index('<kind text="') + kindNum]
        #gotta do the major major minor minor stuff so not 7
        while kind[len(kind) -1] != '7':
            kindNum += 1
            kind = kind + t[t.index('<kind text="') + kindNum]

        degreeValue = t[t.index('<degree-value>') + 14]
        degreeAlter = t[t.index('<degree-alter>') + 14]
        if degreeAlter == '-':
            degreeAlter = degreeAlter + t[t.index('<degree-alter>') + 15]
        degreeTypeIndex = t.index('<degree-alter>') + 1

        noteLetter = t[t.index('<root-step>') + 11]
        noteAlter = t[t.index('<root-alter>') + 13]
        if noteAlter == '-':
            noteAlter = noteAlter + t[t.index('<root-alter>') + 14]

        durationNum = 11
        duration = t[t.index('<duration>') + durationNum]
        while duration[len(duration) -1] != '<':
            durationNum += 1
            duration = duration + t[t.index('<duration>') + durationNum]

        if noteAlter == '-1':
            noteAlter = 'b'
        elif noteAlter == '1':
            noteAlter = '#'

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

        if kind == 'maj7':
            ctype = 'maj'
            seven = 'maj'
        elif kind == 'm7':
            ctype = 'min'
            seven = 'min'
        elif kind == '7':
            ctype = 'maj'
            seven = 'min'
        degree = [degreeValue, degreeAlter]
        #gotta put the degree stuff in a tuple

        fullChord = Chord(note, ctype, seven, degree, duration)
        if i == end_chunk:
            print(fullChord)
        
    return fullChord

writeChord(bfaString)
#print(bfaString)
