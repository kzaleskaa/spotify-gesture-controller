<div align="center">
<h1>SPOTIFY GESTURE CONTROLLER</h1>
<img src="https://user-images.githubusercontent.com/62251989/149663561-90e99712-58a9-40c6-9822-69a7092d582b.png" alt="Spotify Gesture Controller logo"/>
</div>

## 📝 Description

Spotify Gesture Controller is a project realised during "Programming in functional languages" course. The main goal was create the app, which can:

- play/pause current track
- skip to next/previous track
- add/remove song to saved
- volume up/down music

using hand gestures. To do this, **Python 3.9** was used with **OpenCV** and **MediaPipe** libraries. **Tensorflow** model was trained on custom dataset, which was created by myself.

## 🏃‍ How to install and run it?

**Remember: to use this app you need to have premium version of Spotify.**

1. Download repository
   ```
   git clone https://github.com/kzaleskaa/hand-gesture-recognition.git
   cd hand-gesture-recognition
   ```
2. Create a new project at [Spotify Dashboard](https://developer.spotify.com/dashboard/) and edit settings - add `http://localhost:8888/spotify-api/callback/` in Redirect URLs.
3. Create your environment and activate it
   ```bash
   $ python -m venv venv
   ```
4. Install requirements
   ```bash
   $ pip install -r .\requirements.txt
   ```
5. In root project directory, create .env file with following content (from your Spotify Dashboard):
   ```
   CLIENT_ID=<YOUR CLIENT ID>
   CLIENT_SECRET=<YOUR CLIENT SECRET>
   ```
6. Start app
   ```
   python main.py
   ```
7. Open your spotify app, start play music and use this app to control it

## ✋ Gestures

![ezgif com-gif-maker (9)](https://user-images.githubusercontent.com/62251989/150003931-1bb5ec49-8f3a-4c2e-8ed4-a12f89ddafe2.gif)

## 🎶 Spotify API

> Based on simple REST principles, the Spotify Web API endpoints return JSON metadata about music artists, albums, and tracks, directly from the Spotify Data Catalogue.

If no action on Spotify is made, please open your app and start play music manually. Then, you can use this app to control it.

## 🖊 Credits

- Heart photo created by nakaridore - [Freepik](www.freepik.com)
- Icons - [Flaticon](Flaticon.com)
