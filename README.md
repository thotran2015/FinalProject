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
### Installing
All the dependencies you will need are listed in requirement.txt. 
Install the dependencies using Pip:
```
pip install -r requirements.txt
```
### Code
* **menu.py** is the main that you will run to start up the IM app.
* **animation.py** contains Kivy widget and app without any menu or navigation UI


