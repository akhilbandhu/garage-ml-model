#!/usr/bin python
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import atexit
import logging
import os
import sys
import time
import threading

from datetime import datetime


class Capturer():
  def __init__(self):
    pass

  def take_picture(self, capture_night):
    images = []
    with PiCamera(sensor_mode=2) as camera:
      camera.rotation = 270
      camera.resolution = (224, 224)

      img = self._capture(camera)
      images.append(img)

      if capture_night:
        logging.debug("setting up night mode")
        camera.iso = 1600
        camera.framerate = 0.5
        camera.shutter_speed = 5000000
        camera.drc_strength = 'off'
        camera.contrast = 50
        camera.brightness = 70

        img = self._capture(camera)
        images.append(img)

    return images  

  def _capture(self, camera):
    capImg = PiRGBArray(camera)
    time.sleep(2)
    camera.capture(capImg, format = 'bgr')
    ar = capImg.array
    image = Image.fromarray(ar)
    return image
  
