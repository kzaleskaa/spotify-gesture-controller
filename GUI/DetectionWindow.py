# Katarzyna Zaleska
# WCY19IJ1S1
from threading import Thread

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog

from GestureRecognition import GestureRecognition
from queue import Queue
from pyui.DetectionWindow import Ui_DetectionWindow


class DetectionWindow(QDialog, Ui_DetectionWindow):
    """The class represents detection window of GUI."""
    def __init__(self):
        """DetectionWindow constructor"""
        super().__init__()
        self.setupUi(self)
        self.token = ""
        self._connect_buttons()
        self.queue = Queue()
        self.detection = GestureRecognition()

    def _connect_buttons(self) -> None:
        """Function connects button with its action."""
        self.pushButton_2.clicked.connect(self.connection_action)

    def connection_action(self) -> None:
        self.detection.change_image.connect(self.update_image)
        self.detection.change_confidence.connect(self.update_confidence)
        self.detection.change_gesture_name.connect(self.update_gesture_name)
        self.detection.add_gesture.connect(self.add_gesture)
        self.detection.token = self.token
        self.detection.start()

    @pyqtSlot(str)
    def update_confidence(self, confidence: str) -> None:
        """Function updates confidence label.

        Args:
            confidence (str): confidence of detected gesture
        """
        self.detection_confidence.setText(f"Confidence: {confidence}%")

    @pyqtSlot(str)
    def update_gesture_name(self, gesture_name: str) -> None:
        """Function updates label with gesture name.

        Args:
            gesture_name (str): name of detected gesture
        """
        self.detected_gesture_name.setText(f"Gesture name: {gesture_name}")

    @pyqtSlot(QImage)
    def update_image(self, image: QImage) -> None:
        """Function shows image from camera.

        Args:
            image (QImage): converted frame from camera
        """
        self.detection_camera.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(str)
    def add_gesture(self, gesture_name: str) -> None:
        self.q.put(gesture_name)
