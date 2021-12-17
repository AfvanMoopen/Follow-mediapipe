
import mediapipe as mp # Import mediapipe
import cv2 # Import opencv
import pydirectinput
mp_drawing = mp.solutions.drawing_utils # Drawing helpers
mp_holistic = mp.solutions.holistic # Mediapipe Solutions
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 480)
mp_pose = mp.solutions.pose

pose = ""

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False        
        
        # Make Detections
        results = holistic.process(image)
        image.flags.writeable = True   
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        height, width, channel = image.shape
        
        try: 
            right_hand = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * width,
                              results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * height)

            left_hand= (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * width,
                               results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * height)

             
            dist = abs(right_hand[1] - left_hand[1])
            
            if dist > 30 and left_hand[1] < right_hand[1]:
                pose = "Right"    
                pydirectinput.keyUp('left')
                pydirectinput.keyDown('right')
            elif dist > 30 and left_hand[1] > right_hand[1]:
                pose = "Left"
                pydirectinput.keyUp('right')
                pydirectinput.keyDown('left')
            else:
                pose = "move"
        
        except:
            pass

        cv2.putText(image, pose, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0), 3)
        
        
        # Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )
                        
        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
