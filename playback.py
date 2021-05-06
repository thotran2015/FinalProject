#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 16:05:07 2021

@author: thotran
"""
import Leap, sys


import soundfile as sf
import sounddevice as sd
import time 

data, fs = sf.read('click.wav', dtype='float32')
controller = Leap.Controller()

#start = True

#sleep_dur = 1  #sec

def playback_and_visualize_tempo(sleep_dur, dur=50):
    return



def playback_tempo(sleep_dur, dur=50):

    #sd.play(data, fs)
    #time.sleep(5)
    
    start_time = time.time()
    # Create a sample listener and controller
    #listener = SampleListener()
    prev_t = None
    while time.time() - start_time < dur:
        start_ts = time.time()

        if not prev_t is None:
            print('Playing click %.3f seconds after previous ' % (time.time() - prev_t))
        prev_t = time.time()

        sd.play(data, fs)

        frame = controller.frame()
        hand = frame.hands[0]

        print('Stop by making a fist')
        if hand.grab_strength == 1:
            print('Metronome Stopped')
            return False

        time.sleep(sleep_dur - (time.time() - start_ts))

    return False











