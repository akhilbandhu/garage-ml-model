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

import numpy as np

from flask import *
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

POOL_TIME = 5 #Seconds

@app.route('/', methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        mode = request.form.get('mode')
        status = request.form.get('doorStatus')
        print("button pressed: [%s] %s" % (mode, status))
  
        now = datetime.now()
        ts = now.strftime("%Y%m%d_%H%M%S")
        file_name="static/%s/%s" % (status, ts)

        day = "%s_day.jpg" % file_name
        night = None
        if mode=="night":
            night = "%s_night.jpg" % file_name

        take_picture(mode, day, night)

        return redirect(url_for('hello', status=status, ts=ts))
        #return redirect("hello")

    status = request.args.get('status')
    ts = request.args.get('ts')
    return render_template('hello.html', status=status, ts=ts)

def take_picture(mode, day, night):
    with PiCamera(sensor_mode=2) as camera:
        camera.rotation = 270
        camera.resolution = (224, 224)

        capture(camera, day)

        # optionally capture night
        if night:
            print("setting up night mode")
            camera.iso = 1600
            camera.framerate = 0.5
            camera.shutter_speed = 5000000
            camera.drc_strength = 'off'
            camera.contrast = 50
            camera.brightness = 70

            capture(camera, night)

def capture(camera, file):
    capImg = PiRGBArray(camera)
    time.sleep(2)
    camera.capture(capImg,format = 'bgr')
    ar = capImg.array
    print(camera.exposure_speed)
    if file is None:
        return
    print(file)
    image = Image.fromarray(ar)
    image.save(file)
  
    # add text
    #draw = ImageDraw.Draw(image)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 8)
    #draw.text((0, 0),os.path.basename(file),(255,255,255),font=font)
    #image.save("/home/pi/wwwroot/static/latest.jpg")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8081, debug=True)
