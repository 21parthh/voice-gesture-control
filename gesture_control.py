import cv2
import mediapipe as mp
import pyautogui
import numpy as np

class GestureControl:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils
        self.is_running = False
        self.screen_width, self.screen_height = pyautogui.size()

    def start(self):
        self.is_running = True
        cap = cv2.VideoCapture(0)

        while self.is_running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                    x = int(index_tip.x * self.screen_width)
                    y = int(index_tip.y * self.screen_height)
                    pyautogui.moveTo(x, y)
                    self.detect_gestures(hand_landmarks)

            cv2.imshow("Gesture Control", frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def detect_gestures(self, hand_landmarks):
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        distance = ((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2)**0.5

        if distance < 0.05:
            pyautogui.click()
            print("Click detected")

        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        if wrist.x < 0.2:
            pyautogui.hotkey('alt', 'left')
            print("Swipe left detected")
        elif wrist.x > 0.8:
            pyautogui.hotkey('alt', 'right')
            print("Swipe right detected")

        if distance < 0.05 and abs(index_tip.y - thumb_tip.y) < 0.05:
            pyautogui.scroll(10)
            print("Pinch detected")

    def stop(self):
        self.is_running = False
