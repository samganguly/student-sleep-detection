#libraries
import cv2
import os
import numpy as np
from pygame import mixer
import time

def load_model_safe(model_path):
    try:
        import tensorflow as tf
        return tf.keras.models.load_model(model_path)
    except Exception as e1:
        #t2
        try:
            from keras.models import load_model
            return load_model(model_path, compile=False)
        except Exception as e2:
            try:
                import tensorflow as tf
                return tf.keras.models.load_model(model_path, compile=False)
            except Exception as e3:
                print(f"Failed to load model {model_path}: {e3}")
                return None

def main():
    mixer.init()
    
    try:
        sound = mixer.Sound('alarm2.wav')
        print("✓ Alarm sound loaded successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not load alarm sound - {e}")
        sound = None

    try:
        face = cv2.CascadeClassifier('haar cascade files/haarcascade_frontalface_alt.xml')
        leye = cv2.CascadeClassifier('haar cascade files/haarcascade_lefteye_2splits.xml')
        reye = cv2.CascadeClassifier('haar cascade files/haarcascade_righteye_2splits.xml')
        print("✓ Haar cascade classifiers loaded successfully")
    except Exception as e:
        print(f"❌ Error loading Haar cascades: {e}")
        return

    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: Could not open webcam")
            return
        print("✓ Webcam initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing webcam: {e}")
        return

    model = None
    model_paths = ['models/cnn.h5', 'models/cnn_eye_classification.h5']
    
    for model_path in model_paths:
        if os.path.exists(model_path):
            print(f"Trying to load model: {model_path}")
            model = load_model_safe(model_path)
            if model is not None:
                print(f"✓ Model loaded successfully: {model_path}")
                break
            else:
                print(f"❌ Failed to load model: {model_path}")
    
    if model is None:
        print("❌ No models could be loaded. Using simple eye detection without ML.")
        use_ml = False
    else:
        use_ml = True

    score = 0
    font = cv2.FONT_HERSHEY_TRIPLEX
    
    print("\n🚀 Starting sleep detection...")
    print("📷 Make sure you're visible in the webcam")
    if use_ml:
        print("🧠 Using AI model for eye state detection")
    else:
        print("👁 Using basic eye detection (no AI model)")
    print("⚠ When drowsiness is detected, an alarm will sound")
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

            # Convert frame to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces and eyes
            faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
            left_eye = leye.detectMultiScale(gray)
            right_eye = reye.detectMultiScale(gray)

            # Create black rectangle for score display
            cv2.rectangle(frame, (0, height - 80), (300, height), (0, 0, 0), thickness=cv2.FILLED)

            # Draw face rectangles
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

            eyes_detected = len(left_eye) > 0 or len(right_eye) > 0
            
            if use_ml and model is not None:
                # Use ML model for prediction
                rpred = [0.5, 0.5]  
                lpred = [0.5, 0.5]

                # Process right eye
                for (x, y, w, h) in right_eye:
                    r_eye = frame[y:y+h, x:x+w]
                    r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
                    r_eye = cv2.resize(r_eye, (24, 24))
                    r_eye = r_eye / 255
                    r_eye = r_eye.reshape(24, 24, -1)
                    r_eye = np.expand_dims(r_eye, axis=0)
                    try:
                        rpred = model.predict(r_eye, verbose=0)
                    except:
                        rpred = [0.5, 0.5]
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
                    try:
                        lpred = model.predict(l_eye, verbose=0)
                    except:
                        lpred = [0.5, 0.5]
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    break

                # Determine eye status (closed if prediction[0] > prediction[1])
                left_closed = False
                right_closed = False
                
                try:
                    if len(lpred) > 0:
                        if hasattr(lpred[0], '__len__') and len(lpred[0]) > 1:
                            left_closed = lpred[0][0] > lpred[0][1]  # closed > open
                        else:
                            left_closed = float(lpred[0]) > 0.5
                except:
                    left_closed = False
                    
                try:
                    if len(rpred) > 0:
                        if hasattr(rpred[0], '__len__') and len(rpred[0]) > 1:
                            right_closed = rpred[0][0] > rpred[0][1]  # closed > open
                        else:
                            right_closed = float(rpred[0]) > 0.5
                except:
                    right_closed = False
                
                if left_closed or right_closed:
                    score += 1
                    status = "Eyes Closed (AI)"
                    status_color = (0, 0, 255)
                else:
                    score -= 1
                    status = "Eyes Open (AI)"
                    status_color = (0, 255, 0)
            else:
                # Simple detection without ML - just check if eyes are detected
                # If fewer eyes detected than expected, assume they might be closed
                if len(faces) > 0:
                    expected_eyes = len(faces) * 2  # Expect 2 eyes per face
                    detected_eyes = len(left_eye) + len(right_eye)
                    
                    if detected_eyes < expected_eyes * 0.7:  # If less than 70% of expected eyes , can assume possible sleepiness
                        score += 1
                        status = "Possible Sleepiness"
                        status_color = (0, 165, 255)
                    else:
                        score -= 1
                        status = "Eyes Detected"
                        status_color = (0, 255, 0)
                else:
                    score -= 1
                    status = "No Face Detected"
                    status_color = (255, 255, 255)

                # Draw detected eyes
                for (x, y, w, h) in right_eye:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                for (x, y, w, h) in left_eye:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Keep score non-negative
            if score < 0:
                score = 0

            # Display information
            cv2.putText(frame, f'Drowsiness Score: {score}', (10, height-60), font, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f'Status: {status}', (10, height-40), font, 0.6, status_color, 1, cv2.LINE_AA)
            cv2.putText(frame, f'Eyes: L={len(left_eye)} R={len(right_eye)}', (10, height-20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Check for drowsiness (adjust threshold based on detection method)
            threshold = 5 if use_ml else 10
            if score >= threshold:
                # Display drowsiness warning
                cv2.putText(frame, "DROWSINESS DETECTED!", (10, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, "WAKE UP!", (10, 100), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
                
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

            # Display the frame
            window_name = 'Student Sleep Detection System (Fixed)'
            cv2.imshow(window_name, frame)

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
    required_files = [
        'alarm2.wav',
        'haar cascade files/haarcascade_frontalface_alt.xml',
        'haar cascade files/haarcascade_lefteye_2splits.xml',
        'haar cascade files/haarcascade_righteye_2splits.xml'
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
