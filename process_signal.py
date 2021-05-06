#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 18:00:55 2021

@author: thotran
"""
import Leap
from record import record_process_signal
from playback import playback_tempo
import time

controller = Leap.Controller()

while True:
    print('Start the metronome by pinch!')
    frame = controller.frame()
    hand = frame.hands[0]
    print('Pinch strength: ', hand.pinch_strength)
    if hand.pinch_strength == 1:

        T_avg, bpm = record_process_signal()
        time.sleep(T_avg*2)

        stop = playback_tempo(T_avg, dur=50)

        if not stop:
            break







