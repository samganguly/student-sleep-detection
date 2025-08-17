import cv2
import os
from keras.models import load_model
import numpy as np
from pygame import mixer
import time

def main():
    # Configuration
    DROWSINESS_THRESHOLD = 10  # Score threshold for drowsiness detection
    SENSITIVITY = 1  # How quickly score increases/decreases
    
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
        model = load_model('models/cnn_eye_classification.h5')  # Using the kaggle eye dataset model
        print("✓ Enhanced CNN model loaded successfully")
    except Exception as e:
        try:
            model = load_model('models/cnn.h5')  # Fallback to original model
            print("✓ Original CNN model loaded successfully")
        except Exception as e2:
            print(f"❌ Error loading model: {e2}")
            cap.release()
            return

    # Initialize variables
    score = 0
    font = cv2.FONT_HERSHEY_TRIPLEX
    left_eye_closed = False
    right_eye_closed = False
    
    print(f"\n🚀 Starting enhanced sleep detection...")
    print(f"📷 Make sure you're visible in the webcam")
    print(f"👁 Drowsiness threshold: {DROWSINESS_THRESHOLD} points")
    print(f"⚠ When score reaches {DROWSINESS_THRESHOLD}, alarm will sound")
    print(f"🔴 Press 'q' to quit")
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

            # Convert frame to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces and eyes
            faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
            left_eye = leye.detectMultiScale(gray)
            right_eye = reye.detectMultiScale(gray)

            # Create black rectangle for score display
            cv2.rectangle(frame, (0, height - 80), (300, height), (0, 0, 0), thickness=cv2.FILLED)

            # Process right eye
            for (x, y, w, h) in right_eye:
                r_eye = frame[y:y+h, x:x+w]
                r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
                r_eye = cv2.resize(r_eye, (24, 24))
                r_eye = r_eye / 255
                r_eye = r_eye.reshape(24, 24, -1)
                r_eye = np.expand_dims(r_eye, axis=0)
                rpred = model.predict(r_eye, verbose=0)
                # Draw rectangle around detected eye
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, 'R', (x, y-5), font, 0.5, (255, 0, 0), 1)
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
                # Draw rectangle around detected eye
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, 'L', (x, y-5), font, 0.5, (0, 255, 0), 1)
                break

            # Determine eye states (0 = closed, 1 = open)
            if len(lpred) > 0 and np.argmax(lpred) == 0:
                left_eye_closed = True
            else:
                left_eye_closed = False

            if len(rpred) > 0 and np.argmax(rpred) == 0:
                right_eye_closed = True
            else:
                right_eye_closed = False

            # Update score based on eye states
            if left_eye_closed or right_eye_closed:
                score += SENSITIVITY
                eye_status = "Eyes Closing"
                status_color = (0, 165, 255)  # Orange
            else:
                score -= SENSITIVITY
                eye_status = "Eyes Open"
                status_color = (0, 255, 0)  # Green

            # Keep score non-negative
            if score < 0:
                score = 0

            # Calculate drowsiness percentage
            drowsiness_percent = min(100, (score / DROWSINESS_THRESHOLD) * 100)

            # Display information
            cv2.putText(frame, f'Drowsiness Score: {score}/{DROWSINESS_THRESHOLD}', (10, height-60), font, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f'Status: {eye_status}', (10, height-40), font, 0.6, status_color, 1, cv2.LINE_AA)
            cv2.putText(frame, f'Alert Level: {drowsiness_percent:.0f}%', (10, height-20), font, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

            # Draw faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

            # Check for drowsiness
            if score >= DROWSINESS_THRESHOLD:
                # Display major drowsiness warning
                cv2.putText(frame, "WAKE UP! STUDYING TIME!", (50, 100), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
                
                # Play alarm sound
                if sound:
                    try:
                        sound.play()
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

            elif score >= DROWSINESS_THRESHOLD * 0.7:  # Warning at 70% of threshold
                cv2.putText(frame, "Getting Sleepy...", (50, 100), font, 1, (0, 165, 255), 2, cv2.LINE_AA)

            # Display the frame
            cv2.imshow('Enhanced Student Sleep Detection', frame)

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
        print("🏁 Enhanced sleep detection system stopped")

if __name__ == "__main__":
    required_files = [
        'alarm2.wav',
        'haar cascade files/haarcascade_frontalface_alt.xml',
        'haar cascade files/haarcascade_lefteye_2splits.xml',
        'haar cascade files/haarcascade_righteye_2splits.xml'
    ]
    
    model_files = ['models/cnn_eye_classification.h5', 'models/cnn.h5']
    model_found = any(os.path.exists(model) for model in model_files)
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if not model_found:
        missing_files.extend(model_files)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all files are in the correct location.")
    else:
        print("✅ All required files found")
        main()
