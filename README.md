# Hands-Free Mouse: Gesture Recognition-Based Interface

## Overview
The **Hands-Free Mouse** is a gesture recognition-based system that allows users to control their computer cursor using hand gestures, eliminating the need for a physical mouse. This project leverages computer vision and machine learning techniques to detect and interpret hand movements, enabling intuitive and touchless interaction with digital devices. The system is designed to be simple, cost-effective, and accessible, making it suitable for various applications, including accessibility, touchless control in sterile environments, and interactive presentations.

## Key Features
- **Real-Time Gesture Recognition**: Uses OpenCV (`cv2`) and a custom Hand Tracking Module (`HandTrackingModule`) for real-time hand tracking and gesture recognition.
- **Touchless Interaction**: Control your computer cursor, click, scroll, and perform other mouse actions without physical contact.
- **Low Hardware Requirements**: Works with a standard webcam and minimal computational resources.
- **Customizable Gestures**: Supports basic gestures like pointing, clicking, and scrolling, with potential for customization.

## Applications
- **Accessibility**: Provides an alternative input method for individuals with physical disabilities.
- **Hygienic Environments**: Ideal for use in hospitals, kitchens, or clean rooms where touchless interaction is essential.
- **Interactive Presentations**: Enables presenters to control slides and navigate content using hand gestures.
- **Public Kiosks**: Allows touchless navigation in public spaces like malls, airports, and museums.

## System Requirements

### Hardware
- **Camera**: Standard webcam or Raspberry Pi camera module.
- **Processing Unit**: Laptop with at least 4 GB RAM and a 2.0 GHz processor (or Raspberry Pi for low-cost setups).
- **Display**: Monitor or screen for visual feedback.
- **Storage**: 1 GB of available storage for software and libraries.

### Software
- **Operating System**: Windows, Linux, or macOS.
- **Programming Language**: Python.
- **Libraries/Frameworks**:
  - `cv2` (OpenCV) for image processing.
  - `numpy` for numerical operations.
  - `HandTrackingModule` for hand gesture detection.
  - `autopy` and `pyautogui` for simulating mouse actions.
- **IDE**: Visual Studio Code (recommended).

## How to Use
1. **Install Dependencies**:
   ```bash
   pip install opencv-python numpy autopy pyautogui
   ```

2. **Download the HandTrackingModule**:
   Ensure you have the `HandTrackingModule.py` file in your project directory. This module is used for hand detection and tracking.

3. **Run the Application**:
   ```bash
   AIVirtualMouse.py
   ```

4. **Calibrate Gestures**:
   Follow the on-screen instructions to calibrate your hand gestures for cursor movement, clicking, and scrolling.

5. **Start Using**:
   Perform hand gestures in front of the webcam to control the cursor:
   - **Pointing**: Move your hand to control the cursor.
   - **Click**: Perform a specific gesture (e.g., thumb-up) to simulate a mouse click.
   - **Scroll**: Use pinch or swipe gestures to scroll up/down.

## How It Works

### Scrolling
- **Raise your index and middle fingers** (thumb down).
- **Move your fingers up** to scroll up.
- **Move your fingers down** to scroll down.
- The faster you move your fingers, the faster it scrolls.

### Drag and Drop
- **Pinch your index finger and thumb together** and hold to drag.
- **Release the pinch** to drop.

### Left Click
- **Quickly pinch your index finger and thumb together**.

### Right Click
- **Pinch your middle finger and thumb together**.

## Conclusion
The Hands-Free Mouse project demonstrates the potential of gesture-based human-computer interaction as a viable alternative to traditional input devices. By leveraging simple, rule-based algorithms and real-time processing, the system offers an intuitive and accessible way to interact with computers without physical contact. This project is particularly beneficial for individuals with disabilities and environments where touchless interaction is essential.
