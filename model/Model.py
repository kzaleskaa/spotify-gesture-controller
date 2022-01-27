# Katarzyna Zaleska
# WCY19IJ1S1

import os
from typing import Type
import cv2
import mediapipe as mp
import numpy as np
from keras.layers import Dropout
from mediapipe.python.solutions.holistic import Holistic
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical

from constants import ACTIONS, NO_SEQUENCES, DATA_PATH, SEQUENCE_LENGTH


class Model:
    """The class represents the Model created based on the frames from camera. Created model_examples will be saved and used
    to make prediction in GestureRecogniton file. This class isn't used in my app (except of earlier created file
    {model_name}.h5). You can create your own data set and model_examples based on functions below."""

    def __init__(self, model_name: str) -> None:
        """HandDetectionModel constructor.

        Args:
            model_name (str): file name to save the created model
        """
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)
        self.model_name = model_name

    def hand_prediction(self, frame: np.ndarray, model: Holistic) -> Type:
        """Function makes prediction based on holistic model_examples

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

    def create_directory(self) -> None:
        """Function creates directory for every sequence."""
        for action in range(len(ACTIONS)):
            for sequence in range(NO_SEQUENCES):
                try:
                    os.makedirs(os.path.join("../data", DATA_PATH, ACTIONS[action], str(sequence)))
                except Exception as e:
                    print(f"Exception: {e}")

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

    def save_frame(self, results: Type, action: str, sequence: int, frame_num: int) -> None:
        """"Function save frame in appropriate directory.

        Args:
            results (Type): predicted hand
            action (str): action name
            sequence (int): sequence number
            frame_num (int): frame number in sequence
        """
        landmarks = self.save_landmarks(results)
        path = os.path.join("../data", DATA_PATH, action, str(sequence), str(frame_num))
        np.save(path, landmarks)

    def create_dataset(self) -> None:
        """Function creates sequence files for each action by using image from camera."""
        self.create_directory()

        with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            # create frames for every sequence
            for action in ACTIONS:
                for sequence in range(NO_SEQUENCES):
                    cv2.waitKey(1000)
                    print(f"START NEW ACTION: {action}, SEQUENCE NUMBER: {sequence}")
                    for frame_num in range(SEQUENCE_LENGTH):

                        ret, frame = self.cap.read()

                        if not ret:
                            print("Problem with camera...exiting...")
                            break

                        results = self.hand_prediction(frame, holistic)

                        self.create_landmarks(frame, results)

                        self.save_frame(results, action, sequence, frame_num)

                        cv2.imshow("Hand Gesture Recognition - create dataset", frame)

                        if cv2.waitKey(10) & 0xFF == ord('q'):
                            break

            # close all windows and release camera after finish collecting data
            self.cap.release()
            cv2.destroyAllWindows()

    def prepare_data(self) -> tuple:
        """Function creates lists with sequences and appropriate label number.

        Returns:
            tuple: data_sequences -> list with every sequence (for every action);
                    data_labels -> number of label for sequence index
        """
        labels = {ACTIONS[i]: i for i in range(len(ACTIONS))}

        data_sequnces, data_labels = [], []

        for action in ACTIONS:

            for sequnce in range(NO_SEQUENCES):
                frames_in_sequence = []

                for frame_num in range(SEQUENCE_LENGTH):
                    # path with location of frame
                    path = os.path.join("../data", DATA_PATH, action, str(sequnce), f"{frame_num}.npy")
                    loaded_frame = np.load(path)
                    frames_in_sequence.append(loaded_frame)

                # add sequence to data_sequences and choose label name for this sequence
                data_sequnces.append(frames_in_sequence)
                data_labels.append(labels[action])

        data_sequnces = np.array(data_sequnces)
        data_labels = to_categorical(data_labels, dtype="uint8")

        return data_sequnces, data_labels

    def create_model(self) -> None:
        """Function create model_examples based on DATA_PATH and save it to the file model_name.h5"""
        X, y = self.prepare_data()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

        # create an instance of the Sequential class
        model = Sequential()

        # input_shape <- tuple containing the number of timesteps and the number of features
        model.add(LSTM(50, return_sequences=True, activation='relu', input_shape=(30, 126)))
        model.add(Dropout(0.2))
        model.add(LSTM(50, return_sequences=True, activation='relu'))
        model.add(Dropout(0.2))
        model.add(LSTM(50, return_sequences=False, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(6, activation='softmax'))

        model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

        model.fit(X_train, y_train, epochs=100, batch_size=32)

        model.save(f'model_examples/{self.model_name}.h5')

        del model
