import cv2
import mediapipe as mp
import os
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def get_finger_states(hand_landmarks):
    fingers = []
    if hand_landmarks[4].x < hand_landmarks[3].x:  # Thumb
        fingers.append(1)
    else:
        fingers.append(0)
    fingers.append(1 if hand_landmarks[8].y < hand_landmarks[6].y else 0)   # Index
    fingers.append(1 if hand_landmarks[12].y < hand_landmarks[10].y else 0) # Middle
    fingers.append(1 if hand_landmarks[16].y < hand_landmarks[14].y else 0) # Ring
    fingers.append(1 if hand_landmarks[20].y < hand_landmarks[18].y else 0) # Pinky
    return fingers

cap = cv2.VideoCapture(0)
shutdown_triggered = False

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Kamera error")
            continue

        image = cv2.flip(image, 1)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                states = get_finger_states(hand_landmarks.landmark)

                if states == [0, 0, 1, 0, 0]:
                    cv2.putText(image, "NAH JARI TENGAH", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                    if not shutdown_triggered:
                        shutdown_triggered = True
                        print(" jari tengah terdeksi, shutdown dala 3 detik...")
                        time.sleep(3)
                        os.system("shutdown /s /t 0")
                else:
                    shutdown_triggered = False
                    cv2.putText(image, "g ada jari tengah ASUH", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Middle Finger Shutdown Mode", image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
