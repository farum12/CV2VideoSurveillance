# CV2VideoSurveillance
Respository contains implementation of Python script, which turns your Raspberry Pi (with camera) into live-view surveillance IP camera with additional web interface. 
Main feature of the script is motion detection - script recognizes movement on analyzed frame. You can select which part of frame it should analyze in settings.

**Tech Stack:**
- Python
- HTML
- CSS
- Flask
- Jinja2
- OpenCV

# Screenshots
<center><img src="https://user-images.githubusercontent.com/56656135/114100805-231cc780-98c5-11eb-997d-e16e30cbdcec.png" height="500"></center>

<center><img src="https://user-images.githubusercontent.com/56656135/114100813-26b04e80-98c5-11eb-9677-f194b3aab00e.png" height="500"></center>

<center><img src="https://user-images.githubusercontent.com/56656135/114100818-2912a880-98c5-11eb-9de2-0f41d0af7f57.png" height="500"></center>

<center><img src="https://user-images.githubusercontent.com/56656135/114100824-2adc6c00-98c5-11eb-8cd4-45bcdf7d8f84.png" height="500"></center>

# Credits
Section containing authors of certain code snippets, which without this script wouldn't be possible to create. Thank you guys, I really admire your work!
- Adrian Rosebrock, PhD - main feature of script, motion detection using Raspberry Pi camera;
  - https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/
  - https://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/
- Miguel Grinberg - embeeding analyzed frame into Flask:
  - https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited
