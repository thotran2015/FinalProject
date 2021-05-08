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
    def __init__(self, dur, pulsing):
        Widget.__init__(self)
        self.dur = dur
        self.mode = 'Moving Block'
        self.pulsing = pulsing
        self.pulse_schedule = None
        self.button = Button(size_hint=(None, None), text='blob', font_size=32, background_color=[1, 0, 0, 1])
        #if self.pulsing:
            #pass
        #else:
            # with self.canvas:
            #     Color(0, 0, 1)
            #     self.block = Rectangle(size_hint=(None, None))
        with self.canvas:
            Color(0, 0, 1)
            self.block = Rectangle(size_hint=(None, None))

            #self.bind(pos=self.update_rect, size=self.update_rect)
        # if self.pulsing:
        #     self.pulse_schedule = None
        # else:
        #     self.button = Button(size_hint=(None, None), text='blob', font_size=32, background_color=[1, 0, 0, 1])
        #     self.add_widget(self.button)

        #self.add_widget(self.dropdown.mainbutton)

        # Leap Variables
        self.controller = Leap.Controller()
        self.data, self.fs = sf.read('click.wav', dtype='float32')
        self.animation = None
        self.click_schedule = None
        self.controller = Leap.Controller()
        self.state = 'stop'
        self.is_running = False
        self.stop_time = None
        Clock.schedule_interval(self.on_update, 1)

    def play_click(self, dt=None):
        sd.play(self.data, self.fs)

    def blink_square(self, dt=None):
        with self.canvas:
            Color(0, 0, 1)
            Rectangle(size=(900, 700))
            #self.block.size = (900, 700)

        def reset_blink(*args):
            self.canvas.clear()

        Clock.schedule_once(reset_blink)

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
                # time.sleep(2*t_avg)
                Animation.cancel_all(self)
                self.dur = float(round(t_avg, 2))
                print(self.pulsing)
                if self.pulsing:
                    #self.canvas.clear()
                    self.pulse_schedule = Clock.schedule_interval(self.blink_square, self.dur)
                else:
                    self.animation = Animation(pos=(700, 0), duration=0.98 * self.dur) \
                                     + Animation(pos=(0, 0), duration=0.98 * self.dur)
                    self.animation.repeat = True
                    self.animation.start(self.block)
                    #self.animation.start(self.button)

                self.click_schedule = Clock.schedule_interval(self.play_click, self.dur)
                self.is_running = True
                print('Metronome is running. To stop, make a fist!')
            elif self.state == 'stop' and self.is_running:
                print('Metronome Stopped')
                if self.pulsing:
                    self.pulse_schedule.cancel()
                else:
                    self.animation.stop(self.block)
                    self.animation.repeat = False
                self.click_schedule.cancel()
                self.is_running = False
                self.stop_time = time.time()
        else:
            print('Cycle ended! Short waiting before the next cycle!')


class MetronomeApp(App):
    def __init__(self, duration, is_pulsing):
        App.__init__(self)
        self.duration = duration
        self.is_pulsing = is_pulsing

    def build(self):
        self.title = 'Metronome'
        print('Start the metronome by pinch!')
        #dropdown = CustomDropDown()
        #return dropdown
        #return dropdown.vis_dropdown
        return MetronomeWidget(self.duration, self.is_pulsing)


if __name__ == '__main__':
    MetronomeApp(1, True).run()
    print('Hello Jake!')
