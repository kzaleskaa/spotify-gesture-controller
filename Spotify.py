# Katarzyna Zaleska
# WCY19IJ1S1

import requests
from spotipy.oauth2 import SpotifyOAuth

from constants import SCOPE


class SpotifyAPI:
    """The class represents connection with Spotify API."""
    def __init__(self, client_id: str = "", client_secret: str = "", token: str = "", redirect_uri: str = "http://localhost:9000") -> None:
        """SpotifyAPI constructor.

        Args:
            client_id (str): the unique identifier of your app
            client_secret (str): the key you will use to authorize your Web API
            token (str): represents the authorization
            redirect_uri (str): after user approves, where do we send them back to?
        """
        super(SpotifyAPI, self).__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def get_token(self) -> str:
        """Function make authorization and set token"""
        try:
            oauth = SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret,
                          redirect_uri=self.redirect_uri, scope=SCOPE)
            self.token = oauth.get_access_token()['access_token']
            return self.token
        except Exception as e:
            print(f"Exception: {e}")

    def get_playback_state(self) -> dict:
        """Function get information about the user's current playback state,
        including track, progress and active device.

        Returns:
            dict: information about user, track and device
        """
        try:
            endpoint = "https://api.spotify.com/v1/me/player"
            response = requests.get(endpoint, headers=self.headers)
            info = response.json()
            return info
        except Exception as e:
            print(f"Exception: {e}")

    def skip_to_previous(self) -> None:
        """Function skip to previous track"""
        try:
            endpoint = "https://api.spotify.com/v1/me/player/previous"
            requests.post(endpoint, headers=self.headers)
        except Exception as e:
            print(f"Exception: {e}")

    def skip_to_next(self) -> None:
        """Function skip to next track"""
        try:
            endpoint = "https://api.spotify.com/v1/me/player/next"
            requests.post(endpoint, headers=self.headers)
        except Exception as e:
            print(f"Exception: {e}")

    def change_playing_status(self) -> None:
        """Function starts play or pauses music based on current status."""
        try:
            is_playing = self.get_playback_state()['is_playing']

            if is_playing:
                self.pause_playback()
            else:
                self.start_playback()
        except Exception as e:
            print(f"Exception: {e}")

    def pause_playback(self) -> None:
        """Function pauses playing track"""
        try:
            endpoint = "https://api.spotify.com/v1/me/player/pause"
            requests.put(endpoint, headers=self.headers)
        except Exception as e:
            print(f"Exception: {e}")

    def start_playback(self) -> None:
        """Function starts playing paused track"""
        try:
            endpoint = "https://api.spotify.com/v1/me/player/play"
            requests.put(endpoint, headers=self.headers)
        except Exception as e:
            print(f"Exception: {e}")

    def volume_down(self) -> None:
        """Function changes current volume <- current_volume - step """
        step = 5
        try:
            current_volume = self.get_playback_state()['device']['volume_percent']
            volume = current_volume - step if current_volume - step > 0 else 0

            endpoint = "https://api.spotify.com/v1/me/player/volume?volume_percent="
            requests.put(f"{endpoint}{volume}", headers=self.headers)
        except Exception as e:
            print(f"Exception: {e}")

    def volume_up(self) -> None:
        """Function changes current volume <- current_volume + step """
        step = 5
        try:
            current_volume = self.get_playback_state()['device']['volume_percent']
            volume = current_volume + step if current_volume + step < 100 else 100

            endpoint = "https://api.spotify.com/v1/me/player/volume?volume_percent="
            requests.put(f"{endpoint}{volume}", headers=self.headers)
        except Exception as e:
            print(f"Exception: {e}")

    def fav_track(self) -> None:
        """Function checks if current track is in the list of saved track and save or remove it from this list."""
        try:
            items_id = self.saved_tracks_id()

            current_track_id = self.get_playback_state()['item']['id']

            # choose action - save/remove track from the saved songs
            if current_track_id in items_id:
                self.remove_track(current_track_id)
            else:
                self.save_track(current_track_id)
        except Exception as e:
            print(f"Exception: {e}")

    def saved_tracks_id(self) -> list[str]:
        """Function creates list of saved tracks' id"""
        try:
            endpoint = "https://api.spotify.com/v1/me/tracks"
            response = requests.get(f"{endpoint}", headers=self.headers)
            items = response.json()['items']

            # create list with id of saved tracks
            items_id = []
            for e in items:
                items_id.append(e['track']['id'])

            return items_id
        except Exception as e:
            print(f"Exception: {e}")

    def save_track(self, current_track_id: str) -> None:
        """Function adds track to saved playlist.

        Args:
            current_track_id (str): id of currently playing track
        """
        try:
            endpoint = "https://api.spotify.com/v1/me/tracks?ids="
            requests.put(f"{endpoint}{current_track_id}", headers=self.headers)
        except Exception as e:
            print(f"Exception: {e}")

    def remove_track(self, current_track_id: str) -> None:
        """Function removes currently playing track from saved playlist.

        Args:
            current_track_id (str): id of currently playing track
        """
        try:
            endpoint = "https://api.spotify.com/v1/me/tracks?ids="
            requests.delete(f"{endpoint}{current_track_id}", headers=self.headers)
        except Exception as e:
            print(f"Exception: {e}")

    def gesture_action(self, gesture: str) -> None:
        """Function makes action based on gesture name from input_gesture queue.

        Args:
            gesture (str): name of detected gesture
        """
        if gesture == "next":
            self.skip_to_next()
        elif gesture == "prev":
            self.skip_to_previous()
        elif gesture == "love":
            self.fav_track()
        elif gesture == "louder":
            self.volume_up()
        elif gesture == "quieter":
            self.volume_down()
        elif gesture == "play_pause":
            self.change_playing_status()
