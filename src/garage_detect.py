from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import requests
import subprocess
import time

import numpy as np

from PIL import Image
from PIL import ImageEnhance

import tflite_runtime.interpreter as tflite

#TODO: use a context_mananger to dispose the stream
def raspi_capture():
  cmd = "raspistill -w 224 -h 224 -o /home/pi/images/capture.jpg -rot 270 -n -ss 2000000 -br 70 -co 50"
  subprocess.call(cmd, shell=True)
  img = Image.open("/home/pi/images/capture.jpg")
  #img = img.rotate(90)
  # brighten for now
  #enhancer = ImageEnhance.Brightness(img)
  #img = enhancer.enhance(brightness)
  img.save("/home/pi/images/pil.jpg")
  return img

# from: https://support.pushover.app/i44-example-code-and-pushover-libraries#python-image
def send_message(args, img, result, old):
  stream = io.BytesIO()
  img.save(stream, format="jpeg")
  stream.seek(0)

  msg = "%s [%s]" % (result[2], ','.join([x[1][0] for x in old]))
  r = requests.post("https://api.pushover.net/1/messages.json", data = {
    "token": args.app_token,
    "user": args.user_token,
    "message": msg
  },
  files = {
    "attachment": ("image.jpg", stream, "image/jpeg")
  })
  print("sent message: %s" % result[2])
  print(r.text)


class Scorer:
  def __init__(self, model_file, label_file, input_mean, input_std):
    labels = self._load_labels(label_file)
    interpreter = tflite.Interpreter(model_path=model_file)
    interpreter.allocate_tensors()

    # NxHxWxC, H:1, W:2
    self.labels = labels
    self.input_mean = input_mean
    self.input_std = input_std
    self.input_details = interpreter.get_input_details()
    self.output_details = interpreter.get_output_details()
    self.height = self.input_details[0]['shape'][1]
    self.width = self.input_details[0]['shape'][2]  
    self.interpreter = interpreter

    print("init %s x %s" % (self.width, self.height))

  def _load_labels(self, filename):
    with open(filename, 'r') as f:
      return [line.strip() for line in f.readlines()]

  def score(img):
  
    # add N dim
    input_data = np.expand_dims(img, axis=0)
  
    # check the type of the input tensor
    floating_model = self.input_details[0]['dtype'] == np.float32
  
    if floating_model:
      input_data = (np.float32(input_data) - self.input_mean) / self.input_std
  
    self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
  
    self.interpreter.invoke()
  
    output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
    results = np.squeeze(output_data)
  
    top_k = results.argsort()[-5:][::-1]
    result = None
    for i in top_k:
      msg = ""
      if floating_model:
        msg = '{:08.6f}: {}'.format(float(results[i]), self.labels[i])
      else:
        msg = '{:08.6f}: {}'.format(float(results[i] / 255.0), self.labels[i])
      if result is None:
        result = (results[i], self.labels[i], msg)
      print(msg)
    print("---")
    return result


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
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
  parser.add_argument(
      '--brightness',
      default=100, type=int,
      help='brightness')
  parser.add_argument(
      '--user_token',
      default='sometoken',
      help='pushover user token')
  parser.add_argument(
      '--app_token',
      default='sometoken',
      help='pushover app token')

  args = parser.parse_args()

  scorer = Scorer(args.model_file, args.label_file, args.input_mean, args.input_std)

  old_results = []
  last_result = ""
  count = 0
  while True:
    #time.sleep(5)
    img = raspi_capture()
    result = scorer.score(img)
    old_results.append(result)
    if len(old_results) > 10:
      old_results = old_results[-10:]
    
    # ignore low confidence
    if result[0] < 0.6:
      print("ignore low confidence %s" % result[2])
      continue

    # increment and reset on change
    count = count + 1
    if result[1] != last_result:
      count = 0
      last_result = result[1]
      print("reset to %s" % last_result)

    # send message when stable for 30s
    msg = "%s [%s]" % (result[2], ','.join([x[1][0] for x in old_results]))
    print(msg)
    if count == 6:
      send_message(args, img, result, old_results)
  
