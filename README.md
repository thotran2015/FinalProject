# Intuitive Metronome

[comment]: <> (Intuitive Metronome &#40;IM&#41; is an interactive and multimodel metronome that)

[comment]: <> (can take beats from finger snapping, hand clapping, and vocal input and )

[comment]: <> (produce audible clicks at a desired tempo.)
Intuitive Metronome (IM) is an interactive, multimodal metronome that
enables users to express a tempo by snapping fingers, clapping hands,
or vocalizing the rhythm and then produces audible clicks at the desired
tempo. IM can also play accompaniment of a piece of music at a desired 
tempo to simulate a whole orchestra and thus allow users to practice 
with the rest of the instruments at their own pace. 

[comment]: <> (The key ideas behind)

[comment]: <> (IM include tempo detection and gesture recognition. First, tempo )

[comment]: <> (detection is to detect beats per minute &#40;BPM&#41; expressed by snapping,)

[comment]: <> (clapping, vocalizing, etc., and then use that BPM to construct audible)

[comment]: <> (clicks at the desired tempo. Second, the gesture recognition is to)

[comment]: <> (recognize start and stop hand signals that allow users to turn IM )

[comment]: <> (on and off like a conductor.)
## Getting Started
1. Install the Leap Motion SDK for your OS.
   Position the Leap sensor in front of your keyboard 
   and run through a couple of the pre-packaged demos to 
   make sure things are working properly.
2. Download or git clone this repo.
3. IM needs Python 3.5 to run. To simplify the setup process,
   I bundle Python 3.5 and all the dependencies 
   into one conda environment called py35.
   Set up the conda environment py35 using the instructions [below](#setup).
4. If you don't have Linux, please recompile LeapPython for Python 3.5
   in the environment py35. Instructions for recompiling LeapPython is under
   [Recompiling LeapPython for Python 3.5](#recompiling-leappython-for-python-35).
   Note: This process is tedious and requires swig (version 3.0.3) and clang++. 
   This recompiling process is NOT recommended unless you 
   absolutely have no access to Linux.
5. You will need to install libsdl-mixer1.2 for Pygame. 
   Pygame uses an older version of libsdl-mixer, so I could not get it via conda.
   On Linux, use sudo apt to install libsdl-mixer1.2:
   ```
    sudo apt-get install libsdl-mixer1.2 
   ```
   On Mac, use brew (Note: the version on brew is 1.2.15,
   so I think it should work. However, I have not tried this):
   ```
    brew install sdl
   ```


   
   
   
### Setup
Create a conda environment from the py35.yml file.
```
conda env create -f py35.yml
```
This environment contains Python 3.5 and all the dependencies for this project. 
To activate the environment py35: 
```
conda activate py35
```
Once in this environment, you can run
the following command in your terminal to start the IM app:
```
python menu.py
```
If you run the code in PyCharm,
make sure to configure Python interpreter to Python 3.5(py35).

## Code
The main code files are described here. If a file is in the repo but is not described here, 
it probably is not super relevant to the current features of the system.
* **menu.py** is the main that you will run to start up the IM app.
* **animation.py** contains the metronome widget and app without any menu or navigation UI.
* **record.py** is the file that records and process tempo input from users.
* **detect_peaks.py** contains the function that detects peaks in processed signal.
* **midi_player.py** contains code for the accompaniment feature. 
It loads and processes a given midi file. It can adjust the 
  tempo based on the input tempo. Also, it can exclude one 
  instrument from a midi file to simulate the accompaniment of 
  that instrument.
* **testing_filechooser.py** has the filechooser widget 
  for the accompaniment feature.
* **backup** is a folder containing backup copies of
  LeapPython.so and libLeap.dylib that were compiled for Python 3.5 on Linux.
* **midi_files** is a folder with some sample midi files that you can
  use to test out the accompaniment feature. To use your own 
  midi files, save them to this folder.
* **LeapPython.so** is a compiled file of LeapPython module for Python 3.5 and Linux. 
   * Note: If you don't have Linux, please recompile LeapPython for Python 3.5 
   on your OS. Instructions for recompiling LeapPython is under Recompiling LeapPython for Python 3.5.
* **Leap.py** contains Leap SDK functions that return hand positions, pinch/grab strength, etc.
  
## Recompiling LeapPython for Python 3.5
```
# 1) Download Leapmotion SDK 
# 2) Copy Leap.h, LeapMath.h, Leap.i, and libLeap.dylib into one folder.
# 3) Generate LeapPython.cpp with the following command: 
swig -c++ -python -o LeapPython.cpp -interface LeapPython Leap.i
# 4) Compile and link 
clang++ -arch x86_64 -I ${CONDA_PREFIX}/include/python* LeapPython.cpp
 libLeap.dylib ${CONDA_PREFIX}/lib/libpython*.dylib -shared -o LeapPython.so
```
  

