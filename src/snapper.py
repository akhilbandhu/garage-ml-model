from picamera import PiCamera
from time import sleep

camera = PiCamera()

while true:
  camera.capture('/home/pi/wwwroot/static/image.jpg')
  sleep(5)
