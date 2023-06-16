import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

# Initialize counter and body state
rep_counter = 0
body_state = "down"

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)

        # Draw landmark annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

# Define the criteria for a deadlift movement
        if results.pose_landmarks:
    # Get the landmarks for shoulders and hips
         left_shoulder = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
         right_shoulder = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
         left_hip = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
         right_hip = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]

    # Check if the person is in the "down" position
        if body_state == "down":
        # If the shoulders are above the hips, switch the state to "up" and increment the counter
         if left_shoulder.y < left_hip.y and right_shoulder.y < right_hip.y:
            body_state = "up"
            rep_counter += 1
    # If the body state is "up"
        elif body_state == "up":
        # If the shoulders are below the hips, switch the state to "down"
         if left_shoulder.y > left_hip.y and right_shoulder.y > right_hip.y:
            body_state = "down"


        # Display the counter and the body state
        cv2.putText(image, 'Reps: ' + str(rep_counter), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(image, 'Body State: ' + body_state, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the image directly without flipping
        cv2.imshow('MediaPipe Holistic', image)
        if cv2.waitKey(5) & 0xFF == 27:
           break

cap.release()
cv2.destroyAllWindows()
