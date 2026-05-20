import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

st.set_page_config(page_title="AI Rock Paper Scissors", layout="centered")

st.title("AI Rock Paper Scissors Game")
st.write("Show ROCK, PAPER or SCISSOR in front of camera")

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

start = st.checkbox("Start Camera")

frame_window = st.image([])

camera = cv2.VideoCapture(0)

while start:

    success, frame = camera.read()

    if not success:
        st.error("Camera not working")
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    gesture = "No Hand"

    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = hand_landmarks.landmark

            tips = [4, 8, 12, 16, 20]

            fingers = []

            if landmarks[tips[0]].x < landmarks[tips[0] - 1].x:
                fingers.append(1)
            else:
                fingers.append(0)

            for tip in tips[1:]:

                if landmarks[tip].y < landmarks[tip - 2].y:
                    fingers.append(1)

                else:
                    fingers.append(0)

            total_fingers = fingers.count(1)

            if total_fingers == 0:
                gesture = "ROCK"

            elif total_fingers == 5:
                gesture = "PAPER"

            elif total_fingers == 2:

                if fingers[1] == 1 and fingers[2] == 1:
                    gesture = "SCISSOR"

                else:
                    gesture = "UNKNOWN"

            else:
                gesture = "UNKNOWN"

            cv2.putText(
                frame,
                f"Gesture: {gesture}",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3
            )

            cv2.putText(
                frame,
                f"Finger Count: {total_fingers}",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )

    frame_window.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

camera.release()
