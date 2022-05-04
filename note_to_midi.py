
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
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

# class Midi:
#     def __init__(self, duration: int, note: str, velocity: 100): #find a good neutral velocity
#         self.duration = duration
#         self.note = note
#         self.velocity = velocity

#def __init__(self, name: str, pitch = 64, octave = 4, duration = 1)



def convertToMidi(n, bpm):
    song_name = "new_song.mid"
    # declare this new midi file. all messages are on one track
    midi_file = MidiFile(type=0)

    # create a track in the midi file
    track = MidiTrack()
    # put a track in the midi file
    midi_file.tracks.append(track)
    # put in the metamessages for the piece
    track.append(MetaMessage('time_signature', numerator=4, denominator=4,
                             clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(bpm), time=0))
    ticks = midi_file.ticks_per_beat
    track.append(MetaMessage('channel_prefix', channel=0, time=0))
    track.append(MetaMessage('instrument_name', name=' ', time=0))
    for note in n:
        track.append(Message('note_on', channel = 0, note = note.pitch, velocity = 100, time = int(note.duration*ticks)))
        track.append(Message('note_off', channel = 0, note = note.pitch, velocity = 100, time = int(note.duration*ticks)))

    midi_file.save(song_name)

    return song_name
    #gotta figure out what I'm sending this to to play the music
