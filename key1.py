
import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Open the webcam
cap = cv2.VideoCapture(0)

# Define key mapping for a complete keyboard layout
key_mapping = {
    'Q': (50, 100), 'W': (100, 100), 'E': (150, 100), 'R': (200, 100), 'T': (250, 100),
    'Y': (300, 100), 'U': (350, 100), 'I': (400, 100), 'O': (450, 100), 'P': (500, 100),
    'A': (75, 150), 'S': (125, 150), 'D': (175, 150), 'F': (225, 150), 'G': (275, 150),
    'H': (325, 150), 'J': (375, 150), 'K': (425, 150), 'L': (475, 150),
    'Z': (100, 200), 'X': (150, 200), 'C': (200, 200), 'V': (250, 200), 'B': (300, 200),
    'N': (350, 200), 'M': (400, 200), 'SPACE': (275, 250)
}

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Convert the BGR image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    results = hands.process(image)

    # Convert the image back to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates of the index finger tip
            x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * 640)
            y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * 480)

            for key, (kx, ky) in key_mapping.items():
                if abs(x - kx) < 20 and abs(y - ky) < 20:
                    if key == 'SPACE':
                        pyautogui.press(' ')
                    else:
                        pyautogui.press(key)

            # Draw the virtual keyboard
            for key, (kx, ky) in key_mapping.items():
                cv2.putText(image, key, (kx, ky), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Display the image
    cv2.imshow('Virtual Keyboard', image)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
