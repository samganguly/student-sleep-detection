"""
Student Sleep Detection System
Real-time detection of drowsiness using webcam and CNN model
"""

import cv2
import os
from keras.models import load_model
import numpy as np
from pygame import mixer
import time

def main():
    # Initialize pygame mixer for audio
    mixer.init()
    
    # Load alarm sound
    try:
        sound = mixer.Sound('alarm2.wav')
        print("✓ Alarm sound loaded successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not load alarm sound - {e}")
        sound = None

    # Load Haar cascade classifiers
    try:
        face = cv2.CascadeClassifier('haar cascade files/haarcascade_frontalface_alt.xml')
        leye = cv2.CascadeClassifier('haar cascade files/haarcascade_lefteye_2splits.xml')
        reye = cv2.CascadeClassifier('haar cascade files/haarcascade_righteye_2splits.xml')
        print("✓ Haar cascade classifiers loaded successfully")
    except Exception as e:
        print(f"❌ Error loading Haar cascades: {e}")
        return

    # Initialize video capture
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: Could not open webcam")
            return
        print("✓ Webcam initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing webcam: {e}")
        return

    # Load the pre-trained CNN model
    try:
        model = load_model('models/cnn.h5')
        print("✓ CNN model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        cap.release()
        return

    # Initialize variables
    score = 0
    absence_counter = 0
    ABSENCE_THRESHOLD = 30  # Frames without eyes before alarm
    font = cv2.FONT_HERSHEY_TRIPLEX
    last_alarm_time = 0
    alarm_cooldown = 3  # seconds between alarms
    
    print("\n🚀 Starting sleep detection...")
    print("📷 Make sure you're visible in the webcam")
    print("👁 The system will monitor your eye movements")
    print("👀 Will also alert if eyes are not detected (looking away)")
    print("⚠ When drowsiness or absence is detected, an alarm will sound")
    print("🔴 Press 'q' to quit")
    print("-" * 50)

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("❌ Error reading frame from webcam")
                break

            height, width = frame.shape[:2]
            thicc = 2
            rpred = [99]
            lpred = [99]
            current_time = time.time()

            # Convert frame to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces and eyes
            faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
            left_eye = leye.detectMultiScale(gray)
            right_eye = reye.detectMultiScale(gray)

            # Create black rectangle for score display
            cv2.rectangle(frame, (0, height - 80), (250, height), (0, 0, 0), thickness=cv2.FILLED)

            # Check if eyes are detected
            eyes_detected = len(left_eye) > 0 or len(right_eye) > 0
            
            if len(faces) > 0 and eyes_detected:
                # Reset absence counter when eyes are detected
                absence_counter = max(0, absence_counter - 2)

            # Check if eyes are detected
            eyes_detected = len(left_eye) > 0 or len(right_eye) > 0
            
            if len(faces) > 0 and eyes_detected:
                # Reset absence counter when eyes are detected
                absence_counter = max(0, absence_counter - 2)

                # Process right eye
                for (x, y, w, h) in right_eye:
                    r_eye = frame[y:y+h, x:x+w]
                    r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
                    r_eye = cv2.resize(r_eye, (24, 24))
                    r_eye = r_eye / 255
                    r_eye = r_eye.reshape(24, 24, -1)
                    r_eye = np.expand_dims(r_eye, axis=0)
                    rpred = model.predict(r_eye, verbose=0)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    break

                # Process left eye
                for (x, y, w, h) in left_eye:
                    l_eye = frame[y:y+h, x:x+w]
                    l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)
                    l_eye = cv2.resize(l_eye, (24, 24))
                    l_eye = l_eye / 255
                    l_eye = l_eye.reshape(24, 24, -1)
                    l_eye = np.expand_dims(l_eye, axis=0)
                    lpred = model.predict(l_eye, verbose=0)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    break

                # Determine eye status (0 = closed, 1 = open)
                if rpred[0][0] > rpred[0][1] or lpred[0][0] > lpred[0][1]:
                    score += 1
                    status = "Eyes Closed"
                else:
                    score -= 1
                    status = "Eyes Open"
            else:
                # No face or no eyes detected - increment absence counter
                absence_counter += 1
                status = "Eyes Not Detected!"
                # Reduce drowsiness score when no eyes detected
                score = max(0, score - 0.5)

            # Keep score non-negative
            if score < 0:
                score = 0

            # Display score and status
            cv2.putText(frame, f'Drowsiness Score: {score}', (10, height-60), font, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f'Absence Count: {absence_counter}', (10, height-40), font, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, status, (10, 30), font, 0.7, (0, 255, 0) if "Open" in status else (0, 0, 255), 1, cv2.LINE_AA)

            # Draw detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

            # Check for alerts (with cooldown to prevent spam)
            should_alarm = current_time - last_alarm_time > alarm_cooldown

            # Check for drowsiness (score = 1 means sustained eye closure)
            if score >= 1 and should_alarm:
                # Display drowsiness warning
                cv2.putText(frame, "DROWSINESS DETECTED!", (10, height - 80), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                
                # Play alarm sound
                if sound:
                    try:
                        sound.play()
                        last_alarm_time = current_time
                    except:
                        pass

                # Create animated red border
                if thicc < 16:
                    thicc += 2
                else:
                    thicc = thicc - 2
                    if thicc < 2:
                        thicc = 2

                cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), thicc)

            # Check for eye absence (looking away or sleeping with open eyes)
            elif absence_counter >= ABSENCE_THRESHOLD and should_alarm:
                # Display absence warning
                cv2.putText(frame, "EYES NOT DETECTED!", (10, height - 80), font, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, "LOOK AT CAMERA!", (10, 60), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
                
                # Play alarm sound
                if sound:
                    try:
                        sound.play()
                        last_alarm_time = current_time
                    except:
                        pass

                # Create animated blue border for absence detection
                cv2.rectangle(frame, (0, 0), (width, height), (255, 0, 0), 8)

            # Display the frame
            cv2.imshow('Student Sleep Detection System', frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\n⏹ Detection stopped by user")
    except Exception as e:
        print(f"❌ Error during detection: {e}")
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        print("🏁 Sleep detection system stopped")

if __name__ == "__main__":
    # Check if required files exist
    required_files = [
        'alarm2.wav',
        'haar cascade files/haarcascade_frontalface_alt.xml',
        'haar cascade files/haarcascade_lefteye_2splits.xml',
        'haar cascade files/haarcascade_righteye_2splits.xml',
        'models/cnn.h5'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all files are in the correct location.")
    else:
        print("✅ All required files found")
        main()
