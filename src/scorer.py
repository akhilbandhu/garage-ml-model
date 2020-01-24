import numpy as np
import tflite_runtime.interpreter as tflite

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

  def score(self, img):
  
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

