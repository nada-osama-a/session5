import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer
from camera_feed import Camera

class SimpleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(640, 480)

        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        self.setCentralWidget(self.image_label)

        self.camera = Camera()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        frame = self.camera.frame
        if frame is not None:
            h, w, c = frame.shape
            img = QImage(frame.data, w, h, c * w, QImage.Format_BGR888)
            self.image_label.setPixmap(QPixmap.fromImage(img))

    def closeEvent(self, event):
        self.camera.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec())