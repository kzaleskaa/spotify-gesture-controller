# Katarzyna Zaleska
# WCY19IJ1S1

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog

from Connection import Connection
from pyui.DetectionWindow import Ui_DetectionWindow


class DetectionWindow(QDialog, Ui_DetectionWindow):
    """The class represents detection window of GUI."""

    def __init__(self):
        """DetectionWindow constructor"""
        super().__init__()
        self.token = ""
        self.setupUi(self)
        self.connection = Connection(self)
        self._connect_buttons()

    def _connect_buttons(self) -> None:
        """Function connects button with its action."""
        self.pushButton_2.clicked.connect(self.connection_action)

    def connection_action(self) -> None:
        self.connection.change_gesture_name.connect(self.update_gesture_name)
        self.connection.change_confidence.connect(self.update_confidence)
        self.connection.change_image.connect(self.update_image)
        self.connection.token = self.token
        self.connection.started.connect(self.connection.start_detection)
        self.connection.start()

    def destroy_thread(self):
        self.connection.quit()
        self.connection = None

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
