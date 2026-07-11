import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import os
import time

# ----------------------------
# Load Slides - i have folder named slides,within it i have png slide screenshots
# ----------------------------

folder = "slides"

slides = []

for file in sorted(os.listdir(folder)):
    if file.endswith(".jpg") or file.endswith(".png"):
        img = cv2.imread(os.path.join(folder, file))
        slides.append(img)

slideNumber = 0

# Annotation points
annotations = [[]]
annotationNumber = 0
annotationStart = False

# Delay between gestures
buttonPressed = False
buttonCounter = 0
buttonDelay = 20

# Pointer Color
pointerColor = (0,0,255)

# ----------------------------
# MediaPipe
# ----------------------------

mpHands = mp.solutions.hands

hands = mpHands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75
)

mpDraw = mp.solutions.drawing_utils

# Webcam

cap = cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)

# ----------------------------
# Finger Detection
# ----------------------------

tipIds = [4,8,12,16,20]

def fingersUp(lmList):

    fingers=[]

    # Thumb
    if lmList[4][0] > lmList[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers

    for id in range(1,5):

        if lmList[tipIds[id]][1] < lmList[tipIds[id]-2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

# ----------------------------
# Main Loop
# ----------------------------

while True:

    success,img = cap.read()

    img=cv2.flip(img,1)

    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    result=hands.process(imgRGB)

    currentSlide=slides[slideNumber].copy()

    if result.multi_hand_landmarks:

        hand=result.multi_hand_landmarks[0]

        mpDraw.draw_landmarks(img,hand,mpHands.HAND_CONNECTIONS)

        lmList=[]

        h,w,c=img.shape

        for id,lm in enumerate(hand.landmark):

            cx,cy=int(lm.x*w),int(lm.y*h)

            lmList.append((cx,cy))

        fingers=fingersUp(lmList)

        x,y=lmList[8]

        # --------------------------------
        # NEXT SLIDE
        # All fingers up
        # --------------------------------

        if fingers==[1,1,1,1,1] and not buttonPressed:

            if slideNumber < len(slides)-1:

                slideNumber+=1

                annotations=[[]]

                annotationNumber=0

                buttonPressed=True

        # --------------------------------
        # PREVIOUS
        # Only Thumb
        # --------------------------------

        if fingers==[1,0,0,0,0] and not buttonPressed:

            if slideNumber>0:

                slideNumber-=1

                annotations=[[]]

                annotationNumber=0

                buttonPressed=True

        # --------------------------------
        # LASER POINTER
        # Index Finger
        # --------------------------------

        if fingers==[0,1,0,0,0]:

            px=int(np.interp(x,[150,1100],[0,currentSlide.shape[1]]))

            py=int(np.interp(y,[100,650],[0,currentSlide.shape[0]]))

            cv2.circle(currentSlide,(px,py),12,pointerColor,-1)

        # --------------------------------
        # DRAW
        # Index + Middle
        # --------------------------------

        if fingers==[0,1,1,0,0]:

            px=int(np.interp(x,[150,1100],[0,currentSlide.shape[1]]))

            py=int(np.interp(y,[100,650],[0,currentSlide.shape[0]]))

            if annotationStart is False:

                annotationStart=True

                annotationNumber+=1

                annotations.append([])

            annotations[annotationNumber].append((px,py))

        else:

            annotationStart=False

        # --------------------------------
        # CLEAR
        # Pinky Only
        # --------------------------------

        if fingers==[0,0,0,0,1] and not buttonPressed:

            annotations=[[]]

            annotationNumber=0

            buttonPressed=True

        # --------------------------------
        # CUSTOM GESTURE
        # Index + Pinky
        # Starts slideshow
        # --------------------------------

        if fingers==[0,1,0,0,1]:

            pyautogui.press("f5")

    # Draw Annotations

    for annotation in annotations:

        for i in range(len(annotation)-1):

            cv2.line(currentSlide,
                     annotation[i],
                     annotation[i+1],
                     (255,0,0),
                     5)

    # Gesture Delay

    if buttonPressed:

        buttonCounter+=1

        if buttonCounter>buttonDelay:

            buttonCounter=0

            buttonPressed=False

    # Webcam Window

    small=cv2.resize(img,(320,180))

    h,w,_=currentSlide.shape

    currentSlide[0:180,w-320:w]=small

    cv2.imshow("Presentation",currentSlide)

    key=cv2.waitKey(1)

    if key==27:
        break

cap.release()
cv2.destroyAllWindows()
