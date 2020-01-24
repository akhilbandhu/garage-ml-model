#!/usr/bin python
import argparse
import atexit
import base64
from io import BytesIO
import logging
import os
import sys
import time
from threading import Thread, Event

import numpy as np

from flask import *
from flask_bootstrap import Bootstrap
from datetime import datetime

from scorer import Scorer
from notifier import Notifier
from capturer import Capturer
from result_manager import ResultManager

app = Flask(__name__)
Bootstrap(app)

POOL_TIME = 5 #Seconds

@app.route('/', methods=["GET", "POST"])
def root():
    curr_img = result_manager.last_img
    img_str = None
    if curr_img:
      buffered = BytesIO()
      image.save(buffered, format="JPEG")
      img_str = base64.b64encode(buffered.getvalue()) 
    return render_template('display.html', data=img_str)


class MyThread(Thread):
  def __init__(self, event, capturer, scorer, result_manager):
    Thread.__init__(self)
    self.stopped = event
    self.capturer = capturer
    self.scorer = scorer
    self.result_manager = result_manager

  def run(self):
    while not self.stopped.wait(2):
      images = self.capturer.take_picture(True) 

      results = []
      for img in images:
         result = self.scorer.score(img)
         results.append(result)

      self.result_manager.process_results(results, images)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  # model args
  parser.add_argument(
      '-m',
      '--model_file',
      default='/tmp/mobilenet_v1_1.0_224_quant.tflite',
      help='.tflite model to be executed')
  parser.add_argument(
      '-l',
      '--label_file',
      default='/tmp/labels.txt',
      help='name of file containing labels')
  parser.add_argument(
      '--input_mean',
      default=127.5, type=float,
      help='input_mean')
  parser.add_argument(
      '--input_std',
      default=127.5, type=float,
      help='input standard deviation')
 
  # notification args
  parser.add_argument(
      '--user_token',
      default='sometoken',
      help='pushover user token')
  parser.add_argument(
      '--app_token',
      default='sometoken',
      help='pushover app token')
  parser.add_argument(
      '--msg_count',
      default=6, type=int,
      help='send message theshold')

  args = parser.parse_args()


  # construct model scorer
  scorer = Scorer(args.model_file, args.label_file, args.input_mean, args.input_std)
  notifier = Notifier(args.app_token, args.user_token)
  notifier.notify("starting monitor")
  result_manager = ResultManager(0.4, notifier, args.msg_count)
  capturer = Capturer()
  print("starting thread")

  my_event = Event()
  thread = MyThread(my_event, capturer, scorer,result_manager)
  thread.start()
  #app.run(host='0.0.0.0', port=8081, debug=True)
  input1 = input() 
  print("shutting down")
  my_event.set()
  thread.join() 
