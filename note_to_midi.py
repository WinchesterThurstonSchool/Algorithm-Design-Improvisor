
#this video seems really helpful https://www.google.com/search?q=how+to+write+a+midi+file+code&rlz=1C1CHBF_enUS896US896&sxsrf=APq-WBtWl5tqTe4xuplpM2h6gAvZx14JyA%3A1650984471759&ei=FwZoYqL6Lc6HytMPgoeC4AY&ved=0ahUKEwji4d-3_LH3AhXOg3IEHYKDAGwQ4dUDCA4&uact=5&oq=how+to+write+a+midi+file+code&gs_lcp=Cgdnd3Mtd2l6EAMyBQghEKABOgQIABBHOgYIABAWEB46BQgAEIYDOgUIIRCrAjoICCEQFhAdEB5KBAhBGABKBAhGGABQqwFY9Q9ghhFoAHACeACAAZgBiAG9BJIBAzEuNJgBAKABAcgBCMABAQ&sclient=gws-wiz#kpvalbx=_MAZoYufYOvelytMP6fCO0A836
#midi seems pretty similar, just some differences in terminology, specifying an instrument, and duration as determined by buttton presses

#stuff for the class:
#turn the chord into something that can be read as a midi event (on/off(duartion), note, velocity (how hard you hit the button(maybe skip this)))
#establish how much time each chord plays for
#there are different channels in a midi file associated with an instrument. we only need piano
#^^ gotta figure out how to route it through a keyboard package or something (ask marco what program he said he was using)

#fullChord = new Chord(note, ctype, seven, kind, degree, duration)
#converting the chord to a midi event

import pygame
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
import random

# class Midi:
#     def __init__(self, duration: int, note: str, velocity: 100): #find a good neutral velocity
#         self.duration = duration
#         self.note = note
#         self.velocity = velocity

#def __init__(self, name: str, pitch = 64, octave = 4, duration = 1)

song_name = "new_song.mid"
backtrack_name = "A Fine Romance.mp3"

def convertToMidi(n, bpm):
    # declare this new midi file. all messages are on one track
    midi_file = MidiFile(type=0)

    # create a track in the midi file
    track = MidiTrack()
    # put a track in the midi file
    midi_file.tracks.append(track)
    # put in the metamessages for the piece
    track.append(MetaMessage('time_signature', numerator=4, denominator=4))
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(bpm), time=0))
    track.append(MetaMessage('channel_prefix', channel=0, time=0))
    track.append(MetaMessage('instrument_name', name='Piano', time=0))

    for note in n:
        ticks = 120
        if note.duration == 0.0625:
            note.duration = 1
        elif note.duration == 0.125:
            note.duration = 2
        elif note.duration == 0.25:
            note.duration = 4
        elif note.duration == 0.5:
            note.duration = 8
        track.append(Message('note_on', channel = 0, note = note.pitch, velocity = 100, time = 0))
        track.append(Message('note_off', channel = 0, note = note.pitch, velocity = 100, time = int(ticks*note.duration)))

    midi_file.save(song_name)

    return song_name



def play_music(midi_filename):

    # mixer config
    freq = 44100  # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buff = 1024   # number of samples
    pygame.mixer.init(freq, bitsize, channels, buff)

    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)

    # listen for interruptions
    try:
    # use the midi file you just saved
        '''Stream music_file in a blocking manner'''
        clock = pygame.time.Clock()
        pygame.mixer.music.load(midi_filename)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(backtrack_name))
        pygame.mixer.Channel(0).set_volume(.2)
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(30)  # check if playback has finished
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit
