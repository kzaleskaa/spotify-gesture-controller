# Katarzyna Zaleska
# WCY19IJ1S1

from configparser import ConfigParser

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog

from Spotify import SpotifyAPI
from pyui.Authorization import Ui_AuthorizationWindow


class AuthorizationWindow(QDialog, Ui_AuthorizationWindow):
    """Class represents authorization window."""
    def __init__(self):
        """AthorizationWindow constructor"""
        super().__init__()
        self.setupUi(self)
        self._connect_buttons()
        self.setWindowIcon(QIcon('icons/authorization.png'))

    def _connect_buttons(self) -> None:
        """Function connects button with its action."""
        self.submit_btn.clicked.connect(self._on_login_button_clicked)

    def create_submit_message(self, text: str = "", color: str = "#1db954;") -> None:
        """Function changes text of submit_msg label."""
        self.submit_msg.setText(text)
        self.submit_msg.setStyleSheet(f"color: {color}")

    def check_connection(self) -> None:
        """Function checks connection - try to get token based on entered client_id and client_secret
         and show message."""
        self.create_submit_message("Waiting...", "#bbb")
        client_id = self.entered_client_id.text()
        client_secret = self.entered_client_secret.text()
        spotify_account = SpotifyAPI(client_id=client_id, client_secret=client_secret)
        token = spotify_account.get_token()

        if token:
            self.create_submit_message("Successful login!", "#1db954")
            self.save_config(client_id, client_secret, token)
        else:
            self.create_submit_message("Something went wrong.", "red")

        self.entered_client_id.setText("")
        self.entered_client_secret.setText("")

    def save_config(self, client_id: str, client_secret: str, token: str) -> None:
        """Function saves client id, client secret and token to 'config.ini' file."""
        config = ConfigParser()
        config.read('config.ini')
        config.set('CLIENT', 'client_id', client_id)
        config.set('CLIENT', 'client_secret', client_secret)
        config.set('CLIENT', 'token', token)

        with open('config.ini', 'w') as file:
            config.write(file)

    def _on_login_button_clicked(self) -> None:
        """Function makes action after click on login button."""
        self.check_connection()

    def closeEvent(self, event) -> None:
        """Ovverides method to remove entered data."""
        self.entered_client_id.clear()
        self.entered_client_secret.clear()
        self.close()
