import logging

class ResultManager():
  def __init__(self, threshold, notifier, msg_threshold):
    self.notifier = notifier
    self.msg_threshold = msg_threshold
    self.threshold = threshold
    self.old_results = []
    self.last_label = ""
    self.last_notified = "nevernotified"
    self.last_img = None
    self.count = 0
 
  def process_results(self, results, images):
    index = -1    
    if results[0][1] == results[1][1]:
      index = 0
      if results[1][0] > results[0][0]:
        index = 1
    elif results[0][1] != "unknown":
      index = 0
    elif results[1][1] != "unknown":
      index = 1

    if index == -1:
      # both can say, but say different results!
      msg = "CONFLICT [%s], [%s]" % (result[0][2], result[1][2])
      result = (1, "x-CONFLICT", msg) # TODO: always notify or diff threshold?
      self.last_image = None # TODO: combine the images!
    else:
      result = results[index]
      self.last_image = images[index]
  
    # add result to stack
    self.add_result(result)

    # possibly notify
    if self.count == 0:
      self.notify_outlier(index)

    if self.count == self.msg_threshold:
      self.notify()

  # expects a result tuple = (score, label, msg)
  def add_result(self, result):
    result_score = result[0]
    result_label = result[1]
    result_msg = result[2]

    # ignore low confidence
    if result_score < self.threshold:
      logging.info("ignore low confidence %s" % result_msg)
      return

    if len(self.old_results) > 9:
      self.old_results = self.old_results[-9:]
    self.old_results.append(result)

    # increment and reset on change
    self.count = self.count + 1
    if result_label != self.last_label:
      self.count = 0
      self.last_label = result_label
      logging.info("reset to %s" % self.last_label)

  def notify_outlier(self, index):
    result = self.old_results[-1]
    mode = "day"
    if index == 1:
      mode = "night"
    msg = "OUTLIER: %s %s [%s]" % (mode, result[1], result[2])
    self.notifier.notify(msg, self.last_image)

  def notify(self):
    if self.last_label == self.last_notified:
      print("skipping duplicate notification for %s" % self.last_notified)
      return

    msg = "%s [%s]" % (self.last_label, ','.join([x[1][0] for x in self.old_results]))
    self.notifier.notify(msg, self.last_image)
    self.last_notified = self.last_label 

