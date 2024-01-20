from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from GUI.DetectionWindow import DetectionWindow
from pyui.StartWindow import Ui_MainWindow
from components.Spotify import SpotifyAPI


class MainWindow(QMainWindow, Ui_MainWindow):
    """The class represents main window of GUI."""

    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        self.setupUi(self)
        self._connect_buttons()
        self.token = ""
        self.detection_window = DetectionWindow()
        self.spotify_connection = SpotifyAPI()
        self.setWindowIcon(QIcon("icons/sound-waves.png"))

    def _connect_buttons(self) -> None:
        """Function connects button with its action."""
        self.start_btn.clicked.connect(self._on_start_button_clicked)
        self.login_btn.clicked.connect(self._on_login_button_clicked)

    def _on_start_button_clicked(self) -> None:
        """Function opens DetectionWindow."""
        if self.token:
            self.detection_window.token = self.token
            self.detection_window.show()
        else:
            self.label.setText("Please login via Spotify account.")

    def _on_login_button_clicked(self) -> None:
        """Function checks whether user is logged in.

        Returns:
            bool: false - user is not logged in, true in opposite case
        """
        self.spotify_connection.change_token.connect(self.update_token)
        self.spotify_connection.change_msg.connect(self.update_msg)
        self.spotify_connection.start()

    @pyqtSlot(str)
    def update_token(self, token):
        self.token = token

    @pyqtSlot(str)
    def update_msg(self, msg):
        self.label.setText(msg)
