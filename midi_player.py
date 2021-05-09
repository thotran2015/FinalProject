import fluidsynth
import time
import sys
import mido
from mido import MidiFile, tempo2bpm, bpm2tempo, MidiTrack
import pygame
from music21 import converter, note, environment, tempo, clef, stream, instrument, midi, volume
import Leap
from record import record_process_signal
import soundfile as sf
import sounddevice as sd

environment.set('midiPath', '/usr/bin/timidity')
environment.set('musicxmlPath', '/usr/bin/musescore3')

bridge_midi = './midi_files/BridgeOverTroubledWater.mid'
bridge_temp_file = '/tmp/music21/bridge_v1.mid'

data, fs = sf.read('click.wav', dtype='float32')

# mixer config
freq = 44100  # audio CD quality
bitsize = -16  # unsigned 16 bit
channels = 1  # 1 is mono, 2 is stereo
buffer = 1024  # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)


def play_midi_at_tempo(midi_file, bpm, instrument_to_exclude):
    score = converter.parse(midi_file)
    new_score = stream.Score()
    score_list = list(score)
    # score_list[3].show('midi')
    for part in score:
        # part.show('midi')
        # print(part.getInstrument().)
        # if part.getInstrument().midiProgram != 0:
        if part.getInstrument().instrumentName != None and part.getInstrument().instrumentName != instrument_to_exclude:
            if part.getInstrument().instrumentName == 'Mandolin':
                part.insert(0, instrument.StringInstrument())
                # part.insert(0, volume.Volume(velocity=40))

            if part.getInstrument().instrumentName == 'Fretless Bass':
                part.insert(0, instrument.FretlessBass())
                # part.insert(0, volume.Volume(velocity=90))

            if part.getInstrument().instrumentName == 'Alto':
                part.insert(0, instrument.Flute())

            print(part.getInstrument().instrumentName, part.getInstrument().midiProgram)
            for element in part.flat:
                if isinstance(element, tempo.MetronomeMark):
                    print('Original tempo: ', element.number)
                    gain = bpm / element.number
                    element.number *= gain
                    print('New tempo: ', element.number)
            new_score.append(part)
    new_score.write('midi', fp=bridge_temp_file)


play_midi_at_tempo(bridge_midi, 80, 'Piano')


def play_music(midi_filename, controller=None, stop=None):
    '''Stream music_file in a blocking manner'''
    clock = pygame.time.Clock()
    pygame.mixer.music.load(midi_filename)
    '''Play a lead-in click'''
    sd.play(data, fs)
    time.sleep(1)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        if controller:
            frame = controller.frame()
            hand = frame.hands[0]
            print('Make a fist to stop. Pinch strength: ', hand.grab_strength)
            if hand.grab_strength == 1:
                pygame.mixer.music.stop()
        if stop:
            pygame.mixer.music.stop()
        clock.tick(1)  # check if playback has finished


def run_midi_player(bridge_midi, bpm, instrument, controller):
    play_midi_at_tempo(bridge_midi, bpm, instrument)
    # listen for interruptions
    try:
        # use the midi file you just saved
        play_music(bridge_temp_file, controller=controller)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit
    else:
        time.sleep(0.5)


if __name__ == '__main__':
    instruments = ['Piano', 'Cello']

    if len(sys.argv) != 2:
        raise ValueError('Error! Enter the instrument after filename in command. \n e.g. python midi_player.py Piano')

    i = sys.argv[1]
    if i in instruments:
        print('Your instrument: ', i)
        controller = Leap.Controller()
        while True:
            frame = controller.frame()
            hand = frame.hands[0]
            print('Start the metronome by pinch!')
            print('Pinch strength: ', hand.pinch_strength)
            if hand.pinch_strength == 1:
                T_avg, bpm = record_process_signal()
                print('Input BPM: ', bpm)
                play_midi_at_tempo(bridge_midi, bpm, i)
                # listen for interruptions
                try:
                    # use the midi file you just saved
                    play_music(bridge_temp_file, controller)
                except KeyboardInterrupt:
                    # if user hits Ctrl/C then exit
                    # (works only in console mode)
                    pygame.mixer.music.fadeout(1000)
                    pygame.mixer.music.stop()
                    raise SystemExit
            else:
                time.sleep(0.5)
    else:
        msg = 'Instrument not in midi. Give an instrument name from ' + str(instruments)
        raise ValueError(msg)

# n = note.Note("D#3")
# n.duration.type = 'whole'
# n.show('midi')

# littleMelody = converter.parse("tinynotation: 3/4 c4 d8 f g16 a g f#")
# t = tempo.MetronomeMark('adagio')
# littleMelody.insert(0, t)
# print(littleMelody.flat.seconds)
# littleMelody.show('midi')

# mid = MidiFile('./midi_files/bridge3.mid', clip=True)

# new_mid = MidiFile()
# track = MidiTrack()
# new_mid.tracks.append(track)

# for msg in mid:
#     print(msg)
#     if msg.type == "set_tempo":
#         print("before tempo:", tempo2bpm(msg.tempo))
#         msg.tempo = int(bpm2tempo(90))
#         print("after tempo:", tempo2bpm(msg.tempo))
#         msg.time = round(msg.time)
#         track.append(msg)
#     else:
#         msg.time = round(msg.time)
#         track.append(msg)
#
# new_mid.save('./midi_files/60bpm_bridge.mid')

# new_mid = MidiFile('./midi_files/60bpm_bridge.mid')
# for msg in new_mid:
#     if msg.type == "set_tempo":
#         print(msg)
#         print("tempo:", tempo2bpm(msg.tempo))

# print(list(score.flat.notes))
# sp = midi.realtime.StreamPlayer(newscore)
# sp.play()
#
# for part in instrument.partitionByInstrument(score).parts:
# part.show('midi')
# print(score.flat.seconds)
# fctr = 0.5 # scale (in this case stretch) the overall tempo by this factor
# newscore = score.scaleOffsets(fctr).scaleDurations(fctr)
# print(newscore.flat.seconds)

# t = tempo.MetronomeMark(number=208)
# adagio
# print('Ready to Play')
# score.insert(0, t)
#
# for i in score.flat:
#     print(i)
# newscore.show('midi')
# print(score)

# mm1 = tempo.MetronomeMark(number=60)
# n1 = note.Note(type='quarter')
# c1 = clef.AltoClef()
# n2 = note.Note(type='half')
# s1 = stream.Stream()
# s1.append([mm1, n1, c1, n2])
# s1.show('midi')


# fs = fluidsynth.Synth()
# #fs.start()
# ## Your installation of FluidSynth may require a different driver.
# ## Use something like:
# fs.start(driver="pulseaudio")
# sf_file = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
# sfid = fs.sfload(sf_file)
# fs.program_select(0, sfid, 0, 68)
# fs.cc(0, 7, 70)
#
# fs.noteon(0, 60, 100)
# fs.noteon(0, 67, 100)
# #fs.noteon(0, 76, 100)
#
# time.sleep(1.0)
#
# # fs.noteoff(0, 60)
# # fs.noteoff(0, 67)
# # fs.noteoff(0, 76)
# #
# # time.sleep(1.0)
#
# fs.delete()
