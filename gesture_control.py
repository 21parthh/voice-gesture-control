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
        self.is_paused = False
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

            if not self.is_paused and results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    self.handle_cursor_movement(hand_landmarks)
                    self.detect_gestures(hand_landmarks)

            cv2.putText(frame, "Press 'p' to Pause/Resume, 'q' to Quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Gesture Control", frame)

            key = cv2.waitKey(10) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                self.is_paused = not self.is_paused

        cap.release()
        cv2.destroyAllWindows()

    def handle_cursor_movement(self, hand_landmarks):
        """Move the cursor based on the index finger tip position."""
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        x = int(index_tip.x * self.screen_width)
        y = int(index_tip.y * self.screen_height)
        pyautogui.moveTo(x, y)

    def detect_gestures(self, hand_landmarks):
        """Detect specific gestures and perform corresponding actions."""
        if self.is_click_gesture(hand_landmarks):
            pyautogui.click()
            print("Click detected")
        elif self.is_swipe_left(hand_landmarks):
            pyautogui.hotkey('alt', 'left')
            print("Swipe left detected")
        elif self.is_swipe_right(hand_landmarks):
            pyautogui.hotkey('alt', 'right')
            print("Swipe right detected")
        elif self.is_scroll_gesture(hand_landmarks):
            pyautogui.scroll(10)
            print("Scroll detected")
        elif self.is_peace_sign(hand_landmarks):
            pyautogui.hotkey('win', 'up')  # Maximize window
            print("Peace sign detected - Maximize window")
        elif self.is_fist_gesture(hand_landmarks):
            pyautogui.hotkey('alt', 'f4')  # Close window
            print("Fist detected - Close window")

    def is_click_gesture(self, hand_landmarks):
        """Detect click gesture (thumb and index finger close together)."""
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        return self.calculate_distance(thumb_tip, index_tip) < 0.05

    def is_swipe_left(self, hand_landmarks):
        """Detect swipe left gesture (wrist position)."""
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        return wrist.x < 0.2

    def is_swipe_right(self, hand_landmarks):
        """Detect swipe right gesture (wrist position)."""
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        return wrist.x > 0.8

    def is_scroll_gesture(self, hand_landmarks):
        """Detect scroll gesture (pinch with thumb and index finger)."""
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        return self.calculate_distance(thumb_tip, index_tip) < 0.05 and abs(index_tip.y - thumb_tip.y) < 0.05

    def is_peace_sign(self, hand_landmarks):
        """Detect peace sign gesture (index and middle fingers extended, others folded)."""
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        return (
            self.calculate_distance(thumb_tip, middle_tip) > 0.1 and
            self.calculate_distance(thumb_tip, index_tip) > 0.1 and
            ring_tip.y > middle_tip.y and
            pinky_tip.y > middle_tip.y
        )

    def is_fist_gesture(self, hand_landmarks):
        """Detect fist gesture (all fingers close together)."""
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        return (
            self.calculate_distance(thumb_tip, index_tip) < 0.05 and
            self.calculate_distance(thumb_tip, middle_tip) < 0.05
        )

    @staticmethod
    def calculate_distance(point1, point2):
        """Calculate Euclidean distance between two points."""
        return ((point1.x - point2.x)**2 + (point1.y - point2.y)**2)**0.5

    def stop(self):
        self.is_running = False
