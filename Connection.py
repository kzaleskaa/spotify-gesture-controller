# Katarzyna Zaleska
# WCY19IJ1S1

from queue import Queue
from threading import Thread

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QImage

from GestureRecognition import GestureRecognition
from Spotify import SpotifyAPI


class Connection(QThread):
    change_gesture_name = pyqtSignal(str)
    change_confidence = pyqtSignal(str)
    change_image = pyqtSignal(QImage)

    def __init__(self, client_id: str = "", client_secret: str = "", token: str = "") -> None:
        """Connection constructor.

        Args:
            client_id (str): the unique identifier of user app
            client_secret (str): key used to authorize
            token(str):
        """
        super(Connection, self).__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = ""
        self.spotify = ""
        self.hand_detection_model = GestureRecognition("model/nadzieja.h5")

    def start_detection(self) -> None:
        """Function creates threads - detect gestures and make action based on gesture name."""
        q = Queue()
        model_action = Thread(target=self.hand_detection_model.detect_gestures, args=(q, self.change_image,), daemon=True)
        spotify_action = Thread(target=self.gesture_action, args=(q,), daemon=True)

        model_action.start()
        spotify_action.start()

    def gesture_action(self, input_gesture: Queue[str]) -> None:
        """Function makes action based on gesture name from input_gesture queue.

        Args:
            input_gesture (Queue[str]): queue with information about detected gesture
        """
        self.spotify = SpotifyAPI(token=self.token)
        while True:
            gesture_info = input_gesture.get()
            gesture = gesture_info['gesture']
            confidence = gesture_info['confidence']

            if gesture:
                self.change_gesture_name.emit(gesture)
                self.change_confidence.emit(confidence)

                if gesture == "next":
                    self.spotify.skip_to_next()
                elif gesture == "prev":
                    self.spotify.skip_to_previous()
                elif gesture == "love":
                    self.spotify.fav_track()
                elif gesture == "louder":
                    self.spotify.volume_up()
                elif gesture == "quieter":
                    self.spotify.volume_down()
                elif gesture == "play_pause":
                    self.spotify.change_playing_status()
