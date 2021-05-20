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
2. Make sure you have Python 3.5 because you will need 
   Python 3.5 to run IM. 
3. Download or git clone this repo. 
### Installing
All the dependencies you will need are listed in 
requirement.txt. Install the dependencies using Pip:
```
pip install -r requirements.txt
```
### Code
* **menu.py** is the main that you will run to start up the IM app.
* **LeapPython.so** is a compiled file of LeapPython module for Python 3.5 and Linux. 
   * Note: If you don't have Linux, please recompile LeapPython for Python 3.5 
   on your OS. Instructions for recompiling LeapPython is here.
* **animation.py** contains the metronome widget and app without any menu or navigation UI.
* **testing_filechooser.py** has the filechooser widget 
  for the accompaniment feature.
* **backup** is a folder containing backup copies of
  LeapPython.so and libLeap.dylib that were compiled for Python 3.5 on Linux.
* **midi_player** is a folder   

```
# 1) Download Leapmotion SDK 
# 2) Copy Leap.h, LeapMath.h, Leap.i, and libLeap.dylib into one folder.
# 3) Generate LeapPython.cpp with the following command: 
swig -c++ -python -o LeapPython.cpp -interface LeapPython Leap.i
# 4) Compile and link 
clang++ -arch x86_64 -I/Users/iwatobipen/.pyenv/versions/anaconda-2.4.0/include/python3.5 LeapPython.cpp libLeap.dylib /Users/iwatobipen/.pyenv/versions/anaconda-3.5.0/lib/libpython2.7.dylib -shared -o LeapPython.so

```
  

