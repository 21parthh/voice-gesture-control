import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

def detect_gesture():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                if thumb_tip.y < index_tip.y:
                    print("Thumbs up detected!")
                    cap.release()
                    cv2.destroyAllWindows()
                    return "thumbs up"
                
                if thumb_tip.y > index_tip.y:
                    print("Thumbs down detected!")
                    cap.release()
                    cv2.destroyAllWindows()
                    return "thumbs down"
                
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                if wrist.x < 0.2:
                    print("Swipe left detected!")
                    cap.release()
                    cv2.destroyAllWindows()
                    return "scroll up"
                
                if wrist.x > 0.8:
                    print("Swipe right detected!")
                    cap.release()
                    cv2.destroyAllWindows()
                    return "scroll down"

        cv2.imshow('Gesture Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
