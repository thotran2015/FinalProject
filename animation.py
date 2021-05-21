'''
Widget animation
================

This example demonstrates creating and applying a multi-part animation to
a button widget. You should see a button labelled 'plop' that will move with
an animation when clicked.
'''

import kivy

kivy.require('1.0.7')

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
import Leap
import fluidsynth
from record import record_process_signal, record_signal
import time
import soundfile as sf
import sounddevice as sd
from kivy.graphics import Rectangle, Color
from midi_player import run_midi_player
from kivy.uix.label import Label
from kivy.core.window import Window

BLOCK_COLOR = (244/255, 175/255, 27/255, 1)
    #(244/255, 159/255, 28/255, 1)
    #(1, 1, 0, 1)
BG_COLOR = (0/255, 21/255, 79/255, 1)
    #(0, 0, 1, 1)
TEXT_COLOR = (242/255, 188/255, 148/255, 1)

class LeapProcess:
    def __init__(self, thread_queue):
        self.controller = Leap.Controller()
        self.thread_queue = thread_queue
        self.state = 'stop'

    def run(self):
        while True:
            frame = self.controller.frame()
            hand = frame.hands[0]
            if not self.thread_queue.empty():
                continue
            if self.state == 'stop':
                if hand.pinch_strength == 1:
                    self.thread_queue.put('start')
                    self.state = 'start'
            elif self.state == 'start':
                if hand.grab_strength == 1:
                    self.thread_queue.put('stop')
                    self.state = 'stop'


class MetronomeWidget(Widget):
    def __init__(self, dur, pulsing):
        Widget.__init__(self)
        self.dur = dur
        self.mode = 'Moving Block'
        self.pulsing = pulsing
        self.pulse_schedule = None
        self.text_feedback_label = Label(text='Welcome to Intuitive Metronome (IM)!', font_size=26,
                                         bold=True, pos=(350, 300), color=TEXT_COLOR)
        self.text_feedback = 'Welcome to Intuitive Metronome (IM)!'
        self.add_widget(self.text_feedback_label)
        with self.canvas:
            Color(BLOCK_COLOR[0], BLOCK_COLOR[1], BLOCK_COLOR[2], BLOCK_COLOR[3])
            self.block = Rectangle(size_hint=(None, None))
        self.accomp_file = None
        self.accomp_playing = False

        # Leap Variables
        self.controller = Leap.Controller()
        self.data, self.fs = sf.read('click.wav', dtype='float32')
        self.animation = None
        self.click_schedule = None
        self.controller = Leap.Controller()
        self.state = 'stop'
        self.is_running = False
        self.stop_time = None
        self.my_recording = []
        self.gave_recording_feedback = False
        Clock.schedule_interval(self.update_label, 0.5)
        Clock.schedule_interval(self.on_update, 1)

    def update_label(self, *args):
        self.text_feedback_label.text = self.text_feedback

    def play_click(self, dt=None):
        sd.play(self.data, self.fs)

    def blink_square(self, dt=None):
        with self.canvas:
            Color(BLOCK_COLOR[0], BLOCK_COLOR[1], BLOCK_COLOR[2], BLOCK_COLOR[3])
            flash = Rectangle(size=(900, 700))

        def reset_blink(*args):
            self.canvas.remove(flash)

        Clock.schedule_once(reset_blink, self.dur*0.5)

    def process_leap(self):
        frame = self.controller.frame()
        self.hand = frame.hands[0]
        if self.state == 'start':
            if self.hand.grab_strength == 1:
                self.state = 'stop'
        elif self.state == 'stop':
            print('Looking for pinch to start: pinch strength is ', self.hand.pinch_strength)
            self.text_feedback = 'Looking for pinch to start: pinch strength is %s' % round(self.hand.pinch_strength, 2)
            if self.hand.pinch_strength == 1:
                self.state = 'start'

    def on_update(self, *args):
        if (self.stop_time is None) or (time.time() - self.stop_time > 3):
            if self.gave_recording_feedback:
                pass
            else:
                self.process_leap()
            if self.state == 'start' and not self.is_running:
                print('Metronome has started. It is listening for input tempo.')
                if self.accomp_file:
                    self.text_feedback = 'Listening for input tempo. May take awhile to load MIDI file.'
                else:
                    self.text_feedback = 'Metronome has started. It is listening for input tempo.'

                if not self.gave_recording_feedback:
                    self.gave_recording_feedback = True
                else:
                    t_avg, bpm = record_process_signal()
                    self.gave_recording_feedback = False
                    #t_avg, bpm = 0.46, 128
                    if self.accomp_file and not self.accomp_playing:
                        #self.text_feedback = 'Playing MIDI file at your tempo, %s BPM.' % bpm
                        self.py_game = run_midi_player(self.accomp_file, bpm, 'Piano', self.controller)
                        self.accomp_playing = True

                    Animation.cancel_all(self)
                    self.dur = float(round(t_avg, 2))
                    if self.pulsing:
                        if self.block:
                            self.canvas.remove(self.block)
                            self.block = None
                        self.pulse_schedule = Clock.schedule_interval(self.blink_square, self.dur)
                    else:
                        self.animation = Animation(pos=(700, 0), duration=0.98 * self.dur) \
                                         + Animation(pos=(0, 0), duration=0.98 * self.dur)
                        self.animation.repeat = True
                        if self.block is None:
                            with self.canvas:
                                Color(BLOCK_COLOR[0], BLOCK_COLOR[1], BLOCK_COLOR[2], BLOCK_COLOR[3])
                                self.block = Rectangle(size_hint=(None, None))
                        self.animation.start(self.block)

                    self.click_schedule = Clock.schedule_interval(self.play_click, self.dur)
                    self.is_running = True
                    if self.accomp_playing:
                        self.text_feedback = 'Playing MIDI file at your tempo, %s BPM. To stop, make a fist - %s' % (round(bpm), round(self.hand.grab_strength, 2))
                    else:
                        self.text_feedback = 'Metronome is running. To stop, make a fist! Fist strength: %s' % round(self.hand.grab_strength, 2)
                    print('Metronome is running. To stop, make a fist! Fist strength: %s' % round(self.hand.grab_strength, 2))
            elif self.state == 'stop' and self.is_running:
                print('Metronome has stopped')
                self.text_feedback = 'Metronome has stopped.'
                if self.accomp_playing:
                    self.py_game.mixer.music.stop()
                    self.accomp_playing = False
                    self.accomp_file = None

                if self.pulsing:
                    if self.pulse_schedule:
                        self.pulse_schedule.cancel()
                else:
                    if self.animation:
                        self.animation.stop(self.block)
                        self.animation.repeat = False
                if self.click_schedule:
                    self.click_schedule.cancel()
                self.is_running = False
                self.stop_time = time.time()
        else:
            print('Cycle ended! Short waiting before the next cycle!')


class MetronomeApp(App):
    def __init__(self, duration, is_pulsing):
        App.__init__(self)
        Window.clearcolor = BG_COLOR
        self.duration = duration
        self.is_pulsing = is_pulsing

    def build(self):
        self.title = 'Metronome'
        return MetronomeWidget(self.duration, self.is_pulsing)


if __name__ == '__main__':
    MetronomeApp(1, True).run()
    print('Hello Jake!')
