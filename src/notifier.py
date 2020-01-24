import io
import logging
import requests

# from: https://support.pushover.app/i44-example-code-and-pushover-libraries#python-image
class Notifier():
  def __init__(self, app_token, user_token):
    self.app_token = app_token
    self.user_token = user_token

  def notify(self, msg, img=None):
    files = {}
    if img:
      stream = io.BytesIO()
      img.save(stream, format="jpeg")
      stream.seek(0)
      files["attachment"] = ("image.jpg", stream, "image/jpeg")

    r = requests.post("https://api.pushover.net/1/messages.json", data = {
      "token": self.app_token,
      "user": self.user_token,
      "message": msg
    },
    files = files)
    print("sent message: %s" % msg)
    logging.debug(r.text)

