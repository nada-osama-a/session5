from threading import Thread ,Lock
import cv2
import time

class Camera:
    def __init__(self) -> None:
        self.empty_frame = cv2.imread("aur.png") 
        self.capture = cv2.VideoCapture(0) 
        self._frame = None 
        self.is_running = True
        self.lock = Lock()

        self.thread = Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def _capture_loop(self) -> None:
        while self.is_running:
            success, image = self.capture.read()
            if success:
                with self.lock:
                    self._frame = image

            time.sleep(0.01)  # Add a small delay to prevent high CPU usage

    @property
    def frame(self):
        with self.lock:
            return self._frame.copy() if self._frame is not None else self.empty_frame.copy()

    def release(self):
        self.is_running = False
        self.capture.release()