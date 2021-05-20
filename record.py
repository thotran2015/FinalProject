#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 16:33:12 2021

@author: thotran
"""
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from detect_peaks import detect_peaks
import numpy as np
import scipy.signal

def extract_feature_signal(sound_array, hop_size, window_size):
    fea_signal = []
    start = 0
    end = window_size
    while end < len(sound_array):
        fea_signal.append(sum(sound_array[start: end]**2)/window_size)
        start += hop_size
        end = start + window_size
    return fea_signal
        

def record_signal(fs=44100, duration=5):
    # def callback(indata, outdata, frames, time, status):
    #     if status:
    #         print(status)
    #     outdata[:] = indata
    #
    # with sd.Stream(channels=2, callback=callback):
    #     #sd.sleep(int(duration * fs))
    #     sd.rec(int(duration * fs), samplerate=fs, channels=1)
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    return myrecording

def record_process_signal(hop_size = 2048, window_size = 4096, plot_signal=True):
    fs = 44100

    duration = 5  # seconds
    print('Metronome Starts RECORDING')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    # Reshape signal to get signal as 1D array
    sound_array = myrecording.reshape(myrecording.shape[0])

    # Extract energy feature signal
    sqr_sound = extract_feature_signal(sound_array, hop_size, window_size)

    #Extract spectral feature signal
    # t, f, stft = scipy.signal.stft(sound_array, nperseg=window_size, noverlap=hop_size)
    # stft = np.abs(stft)
    # stft_diff = np.diff(stft, axis=1)
    # stft_diff[stft_diff < 0] = 0
    # sqr_sound = np.sum(stft_diff, axis=0)

    # Extract Energy Novel Function (ENF)
    delta_sound = []
    for i in range(len(sqr_sound)-1):
        delta_sound.append(max(sqr_sound[i+1] - sqr_sound[i], 0))

    # Plot original and processed signal
    show_peaks = False
    if plot_signal:
        fig, axes = plt.subplots(1, 3, figsize=(10, 3))
        sound_time = np.arange(len(sound_array))/fs
        axes[0].plot(sound_time, sound_array, label='Raw sound wave')
        axes[0].set_title('Original Signal', fontsize=14)
        axes[0].set_ylabel('Amplitude', fontsize=14)
        axes[0].set_xlabel('Seconds', fontsize=14)
        axes[0].legend()

        feature_time = np.arange(len(sqr_sound)) * hop_size / fs
        enf_time = np.arange(len(delta_sound)) * hop_size / fs
        axes[1].plot(feature_time, sqr_sound, label='Feature')
        axes[1].plot(enf_time, delta_sound, label='ENF')
        axes[1].set_title('Processed Signal', fontsize=14)
        axes[1].set_ylabel('Amplitude', fontsize=14)
        axes[1].set_xlabel('Seconds', fontsize=14)
        axes[1].legend()

        show_peaks = True

    # Detect peaks in the processed sound signal
    peaks = detect_peaks(delta_sound, show=show_peaks, mph=0.05*max(delta_sound), mpd=4, ax=axes[2])
    peaks_time = [enf_time[i] for i in peaks]
    fig.tight_layout()
    fig.savefig('./signal_processing_plots/raw_and_processed_signal.pdf', dpi=300)
    plt.show()


    # Find T_avg by
    #(1) find the delta between two consecutive timestamps in peaks_time
    periods = np.array([peaks_time[i+1] - peaks_time[i] for i in range(len(peaks_time)-1)])

    #(2) Filter out outlier periods
    T_avg = periods.mean()
    T_std = periods.std()
    selected_periods = np.array([p for p in periods if p <= T_avg + 2*T_std and p >= T_avg - 2*T_std])
    print('periods: ', selected_periods)

    assert(len(selected_periods) > 0)

    #(3) Average the timestamp deltas
    selected_T_avg = selected_periods.mean()
    print('average period: ', selected_T_avg)

    # Find BPM, which is (1/T_avg)*(60s/1min)
    bpm = (1/selected_T_avg)*(60)
    print('BPM: ', bpm)
    return selected_T_avg, bpm