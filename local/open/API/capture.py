from datetime import datetime
from time import time
from base64 import b64encode
import cv2


class Capture():
    def __init__(self):
        self.frame_model = {
            'frameId': None,
            'timestamp': None,
            'image': None,
            'site': None
        }

    def frame(self, image, site):
        event_timestamp = datetime.fromtimestamp(int(time()))
        now_string = event_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.frame_model['frameId'] = 'image_%s' % (now_string)
        self.frame_model['timestamp'] = time()
        self.frame_model['image'] = b64encode(
            cv2.imencode('.jpeg', image)[1]).decode()
        self.frame_model['site'] = site
        return self.frame_model
