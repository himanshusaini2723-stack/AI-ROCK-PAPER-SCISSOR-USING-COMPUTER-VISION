#------------------------------------------ROCK , PAPER , SCISSORS GAME USING COMPUTER VISION ----------------------------------------------------------------



#importing libraries

import cv2 #library used for computer vision(live image capturing)
import mediapipe as mp #google Ai based hand tracking library use for gesture recongnition
import random #random library use for random choice of computer from rock,paper scissor


# Mediapipe Setup


mp_hands = mp.solutions.hands #track hand movement using computer vision
hands = mp_hands.Hands( #creates hand detector object
    max_num_hands=1,  #detect 1 hand only
    min_detection_confidence=0.7, #detect only if ai sures more 70% that it is hand
    min_tracking_confidence=0.7 #detection tracking hand while movement if ai sure more than 70%
)
mp_draw = mp.solutions.drawing_utils #use to draw lines on palm to detect object



# Camera Setup


cap = cv2.VideoCapture(0) #open camera using opencv lib 0 means by default webcam

# Bigger Resolution for fullscreen and deployment friendly ui
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# Game Variables


choices = ["Rock", "Paper", "Scissors"] #choices options
computer_choice = "Waiting..." #computer choice by default have waiting before detection
user_choice = "None" #user choice by default none
result = "Show Your Hand" #to prompt user to show hand on screen
game_over = False #track wheather game going on or complete if true then game is over


# Scores


player_score = 0  #score of player and computer increase in each win/loss
computer_score = 0


# Winner Function (decide who win or who loss the game)


def decide_winner(player, computer): #input of user,computer score to update score
    global player_score
    global computer_score
    if player == computer: #condition for draw the game
        return "Draw"
    elif (
        (player == "Rock" and computer == "Scissors") or  #condition of user winning
        (player == "Paper" and computer == "Rock") or
        (player == "Scissors" and computer == "Paper")
    ):
        player_score += 1 #increment score and show message user win
        return "You Win!"
    else:
        computer_score += 1 #if the above conditions draw or user don't win than computer wins
        return "Computer Wins!"


# Main Loop (contnious capture of video detect hands then make game live)


while True:  #infinite loop for game continuity
    success, frame = cap.read()  #web cam detection,works properly stored in success,frame store current captured image
    if not success:   #if camera don't work then came out of loop
        break
    # Mirror Effect
    frame = cv2.flip(frame, 1) #detect hand from different angle by flipping left,right,down,up
    # Dynamic screen size detection for responsive ui
    height, width, _ = frame.shape
    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #opencv default image color format bgr convert to rgb
    # Hand Detection
    results = hands.process(rgb_frame) #send image to ai model for hand detection
    detected_choice = "None" #initially assume no gesture is detected


   
    # Detect Hand
  

    if results.multi_hand_landmarks: #check wheather hand detect in camera or not if detected go inside loop
        for hand_landmarks in results.multi_hand_landmarks: #process detected hand one by one in loop we made max hands 1 so 1 hand can detect
            # Draw Hand Points
            mp_draw.draw_landmarks(   #detect hands features with dots,lines,skeleton type lines
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
            landmarks = hand_landmarks.landmark #store all points of hand in variable
            fingers = [] #list stores finger are open or closed 1. means open 0 means closed
            # Thumb
            if landmarks[4].x < landmarks[3].x: #thumb detection open or close
                fingers.append(1) # if thumb open then in finger list store 1
            else:
                fingers.append(0) #otherwise 0
            # Other Fingers
            tip_ids = [8, 12, 16, 20] #finger tip id's of other 4 fingers
            for tip in tip_ids: #check every finger
                if landmarks[tip].y < landmarks[tip - 2].y: #if finger is higher then open
                    fingers.append(1) #add 1 to finger list
                else:
                    fingers.append(0) #add 0 to finger list means finger closed
            total_fingers = fingers.count(1) #keep track of open fingers in list finger


            # Gesture Logic  (decides the actual guesture on basis of that finger open or closed stored in total_finger store total fingers opened)


            if total_fingers == 0: #if 0 finger open then rock
                detected_choice = "Rock"
            elif total_fingers == 2: #if 2 finger open means scissor
                detected_choice = "Scissors"
            elif total_fingers >= 4:  #if 4 fingers open then paper
                detected_choice = "Paper"
            else:  #else invalid gesture
                detected_choice = "None"

  
    # PLAY ONLY ONE TIME (let user to play only once till it press n for next round)


    if (
        detected_choice != "None" #it checks if choice value become will be rock,paper,scissor then game over
        and game_over == False #if remain none in choice then game not ended
    ):
        user_choice = detected_choice #if game not ended then play round what ai detected rock,paper,scissor then pass as user choice
        computer_choice = random.choice(choices) #random choice made by computer using random library from choices variable that stores[rock,paper,scissor]
        result = decide_winner(user_choice,computer_choice) #passing the value of user choice,computer choice to decide function to find winner
        game_over = True #now game is over

   
    # UI Side Panel (professional responsive ui panel)

    cv2.rectangle(
        frame,
        (0, 0),
        (450, height),
        (0, 0, 0),
        -1
    )


    # Display Text (use to show output or data on camera screen)
  

    cv2.putText(
        frame,
        "AI Rock Paper Scissors", #show message of ai rock,paper,scissor on camera screen
        (40, 60),  #title position
        cv2.FONT_HERSHEY_SIMPLEX, #font style of open cv
        1,   #font size
        (0, 255, 0), # show text in form of bgr format (B,G,R) means green
        3  #text thickness setup
    )

    cv2.putText(  
        frame,
        f"Your Move: {user_choice}",  #shows user's move on screen  f"" fstring is used to to show value of variable along with string without print
        (40, 140), #text position
        cv2.FONT_HERSHEY_SIMPLEX, #font style of open cv
        0.9, #font size
        (0, 255, 255), #show text in form of bgr format (B,G,R) means yellow g+r
        2 #text thickness setup
    )

    cv2.putText(
        frame,
        f"Computer: {computer_choice}", # show computer choice on screen 
        (40, 220),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 0, 0),
        2
    )

    cv2.putText(
        frame,
        f"Result: {result}", #show result keyword on screen
        (40, 300),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

   
    # Scores
   

    cv2.putText(
        frame,
        f"Your Score: {player_score}", #show user's scores on screen
        (40, 420),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Computer Score: {computer_score}", #shows computer score on screen
        (40, 500),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 255),
        2
    )

   
    # Instructions
  

    cv2.putText(
        frame,
        "Rock = closed hand",  #display game instruction to user to close hand for rock
        (40, 620),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Paper = Open Hand",  #open hand for paper
        (40, 660),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Scissors = 2 Fingers", #for scissor show 2 fingers only
        (40, 700),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

   
    # Controls
 

    cv2.putText(
        frame,
        "Press N = Next Round", #press n for next round
        (width - 500, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Press R = Restart Game", #press r for restart
        (width - 500, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "Press Q = Quit", #press q for quit the game
        (width - 500, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

  
    # Fullscreen Window Mode

    cv2.namedWindow(
        "AI Rock Paper Scissors",
        cv2.WND_PROP_FULLSCREEN
    )

    cv2.setWindowProperty(
        "AI Rock Paper Scissors",
        cv2.WND_PROP_FULLSCREEN,
        cv2.WINDOW_FULLSCREEN
    )


    # Show Window (the frame where actual camera screen opens)
    
    cv2.imshow(
        "AI Rock Paper Scissors", #this command creates a frame that shows camera on screen and display message at the top
        frame
    )

   
    # Keyboard Controls (manage keyboard actions like n for next,r for restart,q for quit the game)
  

    key = cv2.waitKey(1) #pass key 1 means detect any key press
    # Next Round
    if key == ord('n'): #if user press n then start next round
        game_over = False #means game not yet over
        computer_choice = "Waiting..." #computer shows wait message for user choice
        user_choice = "None" #user choice by default none
        result = "Show Your Hand" #ask user to show hand
    # Restart Full Game
    if key == ord('r'): # if user press r means restart
        player_score = 0 #scores reset to zero for both player and computer
        computer_score = 0
        game_over = False #game not yet over
        computer_choice = "Waiting..." #computer wait for restart
        user_choice = "None"
        result = "Game Restarted"
    # Quit
    if key == ord('q'): # if user enters q means quit the game break
        break


# Release Resources


cap.release() #release all the variables and resources allocated
cv2.destroyAllWindows() #destroy whole process