import cv2
import mediapipe as mp
import random

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

choices = ["Rock", "Paper", "Scissors"]

computer_choice = "Waiting..."
user_choice = "None"
result = "Show Your Hand"

game_over = False

player_score = 0
computer_score = 0


def decide_winner(player, computer):

    global player_score
    global computer_score

    if player == computer:
        return "Draw"

    elif (
        (player == "Rock" and computer == "Scissors") or
        (player == "Paper" and computer == "Rock") or
        (player == "Scissors" and computer == "Paper")
    ):

        player_score += 1
        return "You Win!"

    else:

        computer_score += 1
        return "Computer Wins!"


while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    height, width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    detected_choice = "None"

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = hand_landmarks.landmark

            fingers = []

            if landmarks[4].x < landmarks[3].x:
                fingers.append(1)

            else:
                fingers.append(0)

            tip_ids = [8, 12, 16, 20]

            for tip in tip_ids:

                if landmarks[tip].y < landmarks[tip - 2].y:
                    fingers.append(1)

                else:
                    fingers.append(0)

            total_fingers = fingers.count(1)

            if total_fingers == 0:
                detected_choice = "Rock"

            elif total_fingers == 2:

                if fingers[1] == 1 and fingers[2] == 1:
                    detected_choice = "Scissors"

            elif total_fingers >= 4:
                detected_choice = "Paper"

            else:
                detected_choice = "None"

    if (
        detected_choice != "None"
        and game_over == False
    ):

        user_choice = detected_choice

        computer_choice = random.choice(choices)

        result = decide_winner(
            user_choice,
            computer_choice
        )

        game_over = True

    cv2.rectangle(
        frame,
        (0, 0),
        (450, height),
        (0, 0, 0),
        -1
    )

    cv2.putText(
        frame,
        "AI Rock Paper Scissors",
        (40, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        3
    )

    cv2.putText(
        frame,
        f"Your Move: {user_choice}",
        (40, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Computer: {computer_choice}",
        (40, 220),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 0, 0),
        2
    )

    cv2.putText(
        frame,
        f"Result: {result}",
        (40, 300),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

    cv2.putText(
        frame,
        f"Your Score: {player_score}",
        (40, 420),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Computer Score: {computer_score}",
        (40, 500),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Rock = Closed Hand",
        (40, 620),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Paper = Open Hand",
        (40, 660),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Scissors = 2 Fingers",
        (40, 700),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Press N = Next Round",
        (width - 500, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Press R = Restart Game",
        (width - 500, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "Press Q = Quit",
        (width - 500, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    cv2.namedWindow(
        "AI Rock Paper Scissors",
        cv2.WND_PROP_FULLSCREEN
    )

    cv2.setWindowProperty(
        "AI Rock Paper Scissors",
        cv2.WND_PROP_FULLSCREEN,
        cv2.WINDOW_FULLSCREEN
    )

    cv2.imshow(
        "AI Rock Paper Scissors",
        frame
    )

    key = cv2.waitKey(1)

    if key == ord('n'):

        game_over = False
        computer_choice = "Waiting..."
        user_choice = "None"
        result = "Show Your Hand"

    if key == ord('r'):

        player_score = 0
        computer_score = 0

        game_over = False

        computer_choice = "Waiting..."
        user_choice = "None"

        result = "Game Restarted"

    if key == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
