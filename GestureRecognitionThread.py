# Katarzyna Zaleska
# WCY19IJ1S1

from typing import Type
import cv2
import mediapipe as mp
import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QImage
from keras.models import load_model
from mediapipe.python.solutions.holistic import Holistic
from Spotify import SpotifyAPI
from constants import ACTIONS, THRESHOLD


class GestureRecognitionThread(QThread):
    """The class represents gesture recognition based on image from camera and created model_examples."""
    def __init__(self, model_name: str = "model/model.h5") -> None:
        """HandDetectionModel constructor.

        Args:
            model_name (str): file name to load the model_examples
        """
        super().__init__()
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.model_name = model_name
        self.token = ""
        self.is_running = True

    change_gesture_name = pyqtSignal(str)
    change_confidence = pyqtSignal(str)
    change_image = pyqtSignal(QImage)
    add_gesture = pyqtSignal(str)
    clear_labels = pyqtSignal()

    def hand_prediction(self, frame: np.ndarray, model: Holistic) -> Type:
        """Function makes prediction based on holistic model.

        Args:
            frame (np.ndarray): frame from camera
            model (Holistic): holistic model_examples used to prediction

        Returns:
            Type: effect of prediction
        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = model.process(frame)
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return results

    def create_landmarks(self, image: np.ndarray, results: Type) -> None:
        """Function draws styled landmarks.

        Args:
            image (np.ndarray): frame from camera
            results (Type): predicted hand
        """
        landmarks_left_hand = self.mp_drawing.DrawingSpec(color=(255, 0, 144), thickness=2, circle_radius=2)
        landmarks_right_hand = self.mp_drawing.DrawingSpec(color=(57, 255, 20), thickness=2, circle_radius=2)
        connection_line = self.mp_drawing.DrawingSpec(thickness=4, color=(90, 90, 90))
        self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                       landmarks_left_hand, connection_line)
        self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                       landmarks_right_hand, connection_line)

    def save_landmarks(self, results: Type) -> np.ndarray:
        """Function creates array with coordinates of landmarks.

        Args:
            results (Type): predicted hand

        Returns:
            np.ndarray: an array object with coordinates of landmarks
        """
        left_hand_points = right_hand_points = np.zeros(63)

        if results.left_hand_landmarks:
            left_hand_points = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten()

        if results.right_hand_landmarks:
            right_hand_points = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten()

        return np.concatenate([left_hand_points, right_hand_points])

    def convert_image(self, image: np.ndarray) -> QImage:
        """Function converts np.ndarray from camera to QImage to display it."""
        RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, _ = RGB_image.shape
        converted_image = QImage(RGB_image.data, w, h, QImage.Format_RGB888)
        scaled_image = converted_image.scaled(600, 600, Qt.KeepAspectRatio)
        return scaled_image

    def run(self) -> None:
        """Function detect gestures based on image from camera and add detected gesture's name to the queue."""
        landmarks_from_frame = []

        model = load_model(self.model_name)

        spotify = SpotifyAPI(token=self.token)

        with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while self.cap.isOpened() and self.is_running:

                ret, frame = self.cap.read()

                if not ret:
                    print("Problem with camera...exiting...")
                    break

                results = self.hand_prediction(frame, holistic)

                self.create_landmarks(frame, results)

                self.change_image.emit(self.convert_image(frame))

                landmarks = self.save_landmarks(results)

                landmarks_from_frame.append(landmarks)

                # get the last 30 elements with landmarks -> 30 frames = sequence
                landmarks_from_frame = landmarks_from_frame[-30:]

                if len(landmarks_from_frame) == 30:
                    transformed_data = np.expand_dims(landmarks_from_frame, axis=0)
                    prediction = model.predict(transformed_data)[0]

                    max_prediction_index = np.argmax(prediction)

                    if prediction[max_prediction_index] > THRESHOLD:
                        confidence = prediction[max_prediction_index]
                        gesture = ACTIONS[max_prediction_index]
                        self.change_gesture_name.emit(gesture)
                        spotify.gesture_action(gesture)
                        self.change_confidence.emit(str(f"{round(confidence*100, 2)}%"))
                        landmarks_from_frame = []

                cv2.waitKey(10)

            self.cap.release()
            self.clear_labels.emit()
