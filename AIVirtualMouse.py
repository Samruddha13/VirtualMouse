import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui

# Webcam settings
wCam, hCam = 640, 480
frameR = 100  # Frame reduction
smoothening = 7  # Smoothness factor

# Variables for smooth motion
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

# Initialize hand detector
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

dragging = False
prevY = 0
scrollBuffer = []
scrollSmoothing = 0.7  # Smoothing factor for scrolling (higher = smoother)
scrollSpeedMultiplier = 3  # Increase scroll speed

while True:
    success, img = cap.read()
    if not success:
        print("Error: Failed to read frame from camera")
        continue

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index finger
        x2, y2 = lmList[12][1:]  # Middle finger
        x4, y4 = lmList[4][1:]  # Thumb

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # Moving Mode: Only index finger up
        if fingers[1] == 1 and fingers[2] == 0 and fingers[4] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # Drag and Drop: Index and thumb held together (PRIORITY 1)
        if fingers[1] == 1 and fingers[4] == 1:
            length, img, lineInfo = detector.findDistance(8, 4, img)
            if length < 40:
                if not dragging:
                    autopy.mouse.toggle(down=True)  # Start dragging
                    dragging = True
                # Move the mouse while dragging
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 255), cv2.FILLED)  # Cyan circle for drag
            else:
                if dragging:
                    autopy.mouse.toggle(down=False)  # Stop dragging
                    dragging = False

        # Left Click: Index and thumb quick pinch (PRIORITY 2)
        if fingers[1] == 1 and fingers[4] == 1 and not dragging:
            length, _, _ = detector.findDistance(8, 4, img)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
                time.sleep(0.15)

        # Right Click: Middle finger and thumb
        if fingers[2] == 1 and fingers[4] == 1:
            length, img, lineInfo = detector.findDistance(12, 4, img)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 0, 255), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)
                time.sleep(0.15)

        # Scroll: Index and middle fingers up
        if fingers[1] == 1 and fingers[2] == 1 and fingers[4] == 0:
            currentY = (y1 + y2) // 2  # Average Y of index and middle fingers

            # Exponential smoothing for fluid motion
            if prevY == 0:
                prevY = currentY
            smoothedY = scrollSmoothing * prevY + (1 - scrollSmoothing) * currentY

            deltaY = prevY - smoothedY  # Inverted for natural scrolling
            scrollSpeed = int(abs(deltaY) * scrollSpeedMultiplier) # Increased speed multiplier

            if abs(deltaY) > 3:  # Smaller deadzone for responsiveness
                if deltaY > 0:
                    pyautogui.scroll(scrollSpeed)  # Scroll up
                    cv2.putText(img, f"↑ Speed: {scrollSpeed}", (20, 120), cv2.FONT_HERSHEY_PLAIN, 2, (100, 255, 100), 2)
                else:
                    pyautogui.scroll(-scrollSpeed)  # Scroll down
                    cv2.putText(img, f"↓ Speed: {scrollSpeed}", (20, 120), cv2.FONT_HERSHEY_PLAIN, 2, (100, 100, 255), 2)

            prevY = smoothedY  # Upevdate prious Y position

    # FPS Display
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('AI Virtual Mouse', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()