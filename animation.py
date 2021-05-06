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
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
import Leap
import fluidsynth
from record import record_process_signal
import time
import soundfile as sf
import sounddevice as sd
from kivy.graphics import Rectangle, Color


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
            # print(hand.grab_strength)
            if self.state == 'stop':
                if hand.pinch_strength == 1:
                    self.thread_queue.put('start')
                    self.state = 'start'
            elif self.state == 'start':
                if hand.grab_strength == 1:
                    self.thread_queue.put('stop')
                    self.state = 'stop'


class MetronomeWidget(Widget):
    def __init__(self, dur):
        Widget.__init__(self)
        self.dur = dur
        self.controller = Leap.Controller()
        self.data, self.fs = sf.read('click.wav', dtype='float32')
        self.animation = None
        self.button = Button(size_hint=(None, None), text='blob', font_size=32, background_color=[1, 0, 0, 1])
        self.add_widget(self.button)
        self.click_schedule = None
        self.controller = Leap.Controller()
        self.state = 'stop'
        self.is_running = False
        self.stop_time = None
        #self.canvas.add(Color(1., 1., 0))
        #self.canvas.add(Rectangle(size=(50, 50)))
        Clock.schedule_interval(self.on_update, 1)

    def play_click(self, dt=None):
        sd.play(self.data, self.fs)

    def blink_square(self, dt=None):
        #self.button.background_color = (0, 0, 1, 1)
        anim = Animation(animated_color=[1, 0, 0, 1]) + Animation(animated_color=[1, 1, 1, 1])
        anim.repeat = True
        anim.start(self)


    def process_leap(self):
        frame = self.controller.frame()
        hand = frame.hands[0]
        if self.state == 'start':
            if hand.grab_strength == 1:
                self.state = 'stop'
        elif self.state == 'stop':
            print('Looking for pinch to start: pinch strength is ', hand.pinch_strength)
            if hand.pinch_strength == 1:
                self.state = 'start'

    def on_update(self, *args):
        if (self.stop_time is None) or (time.time() - self.stop_time > 3):
            self.process_leap()
            if self.state == 'start' and not self.is_running:
                print('Metronome Starts')
                t_avg, bpm = record_process_signal()
                time.sleep(2*t_avg)
                Animation.cancel_all(self)
                self.dur = float(t_avg)
                if self.pulsing:
                    Clock.schedule_interval(self.blink_square, self.dur)
                else:
                    #self.animation = Animation(pos=(700, 0), duration=0.98 * self.dur) \
                    #                 + Animation(pos=(0, 10), duration=0.98 * self.dur)

                    #self.animation.repeat = True
                    #self.animation.start(self.button)


                self.click_schedule = Clock.schedule_interval(self.play_click, self.dur)
                self.is_running = True
                print('Metronome is running. To stop, make a fist!')
            elif self.state == 'stop' and self.is_running:
                print('Metronome Stopped')
                
                #self.animation.stop(self.button)
                #self.animation.repeat = False
                self.click_schedule.cancel()
                self.is_running = False
                self.stop_time = time.time()
        else:
            print('Cycle ended! Short waiting before the next cycle!')


class MetronomeApp(App):
    def __init__(self, duration):
        App.__init__(self)
        self.duration = duration

    def build(self):
        print('Start the metronome by pinch!')
        return MetronomeWidget(self.duration)


if __name__ == '__main__':
    MetronomeApp(1).run()
    print('Hello Jake!')
