import cv2
import mediapipe as mp
import numpy as np

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = float(detectionCon)  # Convert to float
        self.trackCon = float(trackCon)  # Convert to float

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.lmList = []  # Define lmList in constructor

    def findHands(self, img, draw=True):
        if img is None:
            print("Error: Image is empty, skipping frame")
            return img

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []  # Reset lmList for each frame
        xList, yList = [], []  # Store x and y coordinates separately

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])  # Store landmarks in self.lmList
                xList.append(cx)
                yList.append(cy)
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            # Bounding box around hand
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = [xmin, ymin, xmax, ymax]

            return self.lmList, bbox

        return self.lmList, None  # Return None for bbox if no hand detected

    def fingersUp(self):
        fingers = []
        tipIds = [4, 8, 12, 16, 20]

        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                fingers = [1 if hand.landmark[tip].y < hand.landmark[tip - 2].y else 0 for tip in tipIds]

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=10, t=3):
        if len(self.lmList) > max(p1, p2):  # Ensure p1 and p2 exist
            x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
            x2, y2 = self.lmList[p2][1], self.lmList[p2][2]

            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            if draw:
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
                cv2.circle(img, (x1, y1), r, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), r, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (cx, cy), r, (0, 255, 0), cv2.FILLED)

            length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            return length, img, [x1, y1, x2, y2, cx, cy]

        return 0, img, [0, 0, 0, 0, 0, 0]  # Return default values if no landmarks
