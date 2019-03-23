#!/usr/bin/env python
# Create spectogram from audio file

# Libraries
import os
import sys
import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import subprocess
from shutil import copy2 as cp

# Colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Read in last argument as music file
music_file = sys.argv[-1]

# Define output file name
outname=os.path.splitext(os.path.basename(music_file))[0]
dirname=os.path.dirname(music_file)
wavname=(dirname+'/'+outname+'.wav').replace(" ", "_")

# ffmpeg does not work with spaces, copy to tmp file
music_file_tmp=music_file.replace(" ", "_")
cp(music_file, music_file_tmp)

# Convert music file to wav
print bcolors.FAIL + "\n--> CONVERTING MUSIC FILE TO WAV\n" + bcolors.ENDC
command="ffmpeg -i %s -ar 44100 -ac 1 %s" % (music_file_tmp, wavname)
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

# Create spectogram
print bcolors.FAIL + "\n--> CREATE SPECTOGRAM\n" + bcolors.ENDC

# Get file info   
def get_wav_info(wavname):
    wav = wave.open(wavname, 'r')
    frames = wav.readframes(-1)
    sound_info = np.fromstring(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate

# Define function for plotting
def graph_spectrogram(wavname):
    sound_info, frame_rate = get_wav_info(wavname)
    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['savefig.facecolor'] = 'black'
    plt.rcParams['axes.edgecolor'] = 'white'
    plt.rcParams['lines.color'] = 'white'
    plt.rcParams['text.color'] = 'white'    
    plt.rcParams['xtick.color'] = 'white'    
    plt.rcParams['ytick.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    fig = plt.figure(num=None, figsize=(12, 7.5), dpi=300)
    ax = fig.add_subplot(111)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1000))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(500))
    ax.tick_params(axis='both', direction='inout')
    plt.title('Spectrogram of:\n %r' % os.path.basename(music_file))
    plt.xlabel('time in seconds')
    plt.ylabel('Frequency (Khz)')
    plt.specgram(sound_info, Fs=frame_rate, cmap='gnuplot')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('dB')
    plt.savefig(dirname+'/'+outname+'.png')

# Save spectrogram
graph_spectrogram(wavname)

# Remove wav file and temporary file
os.remove(wavname)
os.remove(music_file_tmp)

