# Katarzyna Zaleska
# WCY19IJ1S1

from configparser import ConfigParser
from typing import Any

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from GUI.Authorization import AuthorizationWindow
from GUI.DetectionWindow import DetectionWindow
from Spotify import SpotifyAPI
from pyui.StartWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """The class represents main window of GUI."""

    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        self.setupUi(self)
        self._connect_buttons()
        self.path = "config.ini"
        self.login = None
        self.detection_window = DetectionWindow()
        self.auth_window = AuthorizationWindow()
        self.setWindowIcon(QIcon('icons/sound-waves.png'))

    def _connect_buttons(self) -> None:
        """Function connects button with its action."""
        self.start_btn.clicked.connect(self._on_start_button_clicked)
        self.login_btn.clicked.connect(self._on_auth_button_clicked)

    def _on_auth_button_clicked(self) -> None:
        """Function opens AuthorizationWindow."""
        self.auth_window.show()

    def _on_start_button_clicked(self) -> None:
        """Function opens DetectionWindow."""
        if self._log_in():
            self.detection_window.show()
        else:
            self._on_auth_button_clicked()

    def _log_in(self) -> Any:
        """Function checks whether user is logged in.

        Returns:
            bool: false - user is not logged in, true in opposite case
        """
        client_id, client_secret = self._read_config()

        if len(client_id) > 0 and len(client_secret) > 0:
            spotify_connection = SpotifyAPI(client_id=client_id, client_secret=client_secret)
            if spotify_connection.get_token():
                self.save_token(spotify_connection.token)
                self.login = spotify_connection.token
                self.detection_window.token = spotify_connection.token
            return True
        return False

    def save_token(self, token: str) -> None:
        config = ConfigParser()
        config.read(self.path)
        config.set('CLIENT', 'token', token)

        with open('config.ini', 'w') as file:
            config.write(file)

    def _read_config(self) -> tuple:
        """Function reads information about user from config.ini"""
        parser = ConfigParser()
        parser.read(self.path)
        client_id = parser.get("CLIENT", 'client_id')
        client_secret = parser.get('CLIENT', 'client_secret')
        return client_id, client_secret
