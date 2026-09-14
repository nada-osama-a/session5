import cv2

class Camera:
    def __init__(self) -> None:
        self.empty_frame = cv2.imread("aur.png") 
        self.capture = cv2.VideoCapture(0) 
        
    def get_frame(self):

        success, image = self.capture.read()
        if success:
            return image
        return self.empty_frame


##############################
from threading import Thread
import time
import cv2

class Camera:
    def __init__(self) -> None:
        self.empty_frame = cv2.imread("aur.png")
        self.capture = cv2.VideoCapture(0)
        self._frame = None

        self.thread = Thread(target=self._read_camera_loop, daemon=True)
        self.thread.start()

    def _read_camera_loop(self) -> None:
        while self.is_running:
            success, image = self.capture.read()
            if success:
                self._frame = image

            time.sleep(0.01)

    @property
    def frame(self):
        return self._frame if self._frame is not None else self.empty_frame
