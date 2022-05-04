
#this video seems really helpful https://www.google.com/search?q=how+to+write+a+midi+file+code&rlz=1C1CHBF_enUS896US896&sxsrf=APq-WBtWl5tqTe4xuplpM2h6gAvZx14JyA%3A1650984471759&ei=FwZoYqL6Lc6HytMPgoeC4AY&ved=0ahUKEwji4d-3_LH3AhXOg3IEHYKDAGwQ4dUDCA4&uact=5&oq=how+to+write+a+midi+file+code&gs_lcp=Cgdnd3Mtd2l6EAMyBQghEKABOgQIABBHOgYIABAWEB46BQgAEIYDOgUIIRCrAjoICCEQFhAdEB5KBAhBGABKBAhGGABQqwFY9Q9ghhFoAHACeACAAZgBiAG9BJIBAzEuNJgBAKABAcgBCMABAQ&sclient=gws-wiz#kpvalbx=_MAZoYufYOvelytMP6fCO0A836
#midi seems pretty similar, just some differences in terminology, specifying an instrument, and duration as determined by buttton presses

#stuff for the class:
#turn the chord into something that can be read as a midi event (on/off(duartion), note, velocity (how hard you hit the button(maybe skip this)))
#establish how much time each chord plays for
#there are different channels in a midi file associated with an instrument. we only need piano
#^^ gotta figure out how to route it through a keyboard package or something (ask marco what program he said he was using)

#fullChord = new Chord(note, ctype, seven, kind, degree, duration)
#converting the chord to a midi event
import mido
from mido import Message, MetaMessage, MidiFile, MidiTrack

# class Midi:
#     def __init__(self, duration: int, note: str, velocity: 100): #find a good neutral velocity
#         self.duration = duration
#         self.note = note
#         self.velocity = velocity

#def __init__(self, name: str, pitch = 64, octave = 4, duration = 1)
def convertToMidi(n):
    Message('note_on', channel=0, note = n.pitch, velocity = 100, time = n.duartion)
    #gotta figure out what I'm sending this to to play the music
