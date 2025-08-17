"""
Enhanced Student Sleep Detection System with Eye Absence Detection
- Detects drowsiness when eyes are closed
- Detects inattention when eyes are not visible in camera
- Includes pause/resume functionality
- Enhanced UI with controls
"""

import cv2
import os
import numpy as np
from pygame import mixer
import time

def load_model_safe(model_path):
    """Safely load Keras model with compatibility fixes"""
    try:
        import tensorflow as tf
        return tf.keras.models.load_model(model_path)
    except Exception as e1:
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

def draw_button(frame, text, x, y, width, height, color, text_color=(255, 255, 255)):
    """Draw a button on the frame"""
    cv2.rectangle(frame, (x, y), (x + width, y + height), color, -1)
    cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 255), 2)
    
    # Calculate text position to center it
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    text_size = cv2.getTextSize(text, font, font_scale, 1)[0]
    text_x = x + (width - text_size[0]) // 2
    text_y = y + (height + text_size[1]) // 2
    
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, 1, cv2.LINE_AA)
    
    return (x, y, width, height)

def is_point_in_button(x, y, button_rect):
    """Check if a point is inside a button rectangle"""
    bx, by, bw, bh = button_rect
    return bx <= x <= bx + bw and by <= y <= by + bh

def mouse_callback(event, x, y, flags, param):
    """Handle mouse clicks for buttons"""
    if event == cv2.EVENT_LBUTTONDOWN:
        pause_button, sensitivity_up, sensitivity_down, state = param
        
        if is_point_in_button(x, y, pause_button):
            # Toggle pause state
            state['paused'] = not state['paused']
        elif is_point_in_button(x, y, sensitivity_up):
            # Increase sensitivity (lower threshold)
            if state['absence_threshold'] > 5:
                state['absence_threshold'] -= 5
        elif is_point_in_button(x, y, sensitivity_down):
            # Decrease sensitivity (higher threshold)
            if state['absence_threshold'] < 100:
                state['absence_threshold'] += 5

def main():
    # Configuration
    DROWSINESS_THRESHOLD = 15  # Score threshold for drowsiness (eyes closed)
    ABSENCE_THRESHOLD = 30     # Frames threshold for eye absence detection
    SENSITIVITY = 1            # How quickly score increases/decreases
    
    # State variables
    state = {
        'paused': False,
        'absence_threshold': ABSENCE_THRESHOLD,
        'drowsiness_threshold': DROWSINESS_THRESHOLD
    }
    
    # Initialize pygame mixer for audio
    mixer.init()
    
    # Load alarm sounds
    try:
        drowsy_sound = mixer.Sound('alarm2.wav')
        print("✓ Drowsiness alarm loaded successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not load drowsiness alarm - {e}")
        drowsy_sound = None
    
    try:
        # Try to load a different alarm for absence (or use the same one)
        absence_sound = mixer.Sound('TFALARM.WAV') if os.path.exists('TFALARM.WAV') else drowsy_sound
        print("✓ Absence alarm loaded successfully")
    except Exception as e:
        print(f"⚠ Warning: Using same alarm for absence detection")
        absence_sound = drowsy_sound

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
    model = None
    model_paths = ['models/cnn_eye_classification.h5', 'models/cnn.h5']
    
    for model_path in model_paths:
        if os.path.exists(model_path):
            print(f"Trying to load model: {model_path}")
            model = load_model_safe(model_path)
            if model is not None:
                print(f"✓ Model loaded successfully: {model_path}")
                break
            else:
                print(f"❌ Failed to load model: {model_path}")
    
    use_ml = model is not None

    # Initialize variables
    drowsiness_score = 0
    absence_counter = 0
    font = cv2.FONT_HERSHEY_TRIPLEX
    font_small = cv2.FONT_HERSHEY_SIMPLEX
    last_alarm_time = 0
    alarm_cooldown = 3  # seconds between alarms
    
    print(f"\n🚀 Starting enhanced sleep detection...")
    print(f"📷 Make sure you're visible in the webcam")
    print(f"👁 Drowsiness detection: ON")
    print(f"👀 Eye absence detection: ON")
    print(f"⏸️ Click 'PAUSE' button to pause/resume")
    print(f"🔧 Use +/- buttons to adjust sensitivity")
    print(f"🔴 Press 'q' to quit")
    print("-" * 50)

    # Create window and set mouse callback
    window_name = 'Enhanced Sleep Detection with Eye Absence Alert'
    cv2.namedWindow(window_name)
    
    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("❌ Error reading frame from webcam")
                break

            height, width = frame.shape[:2]
            thicc = 2
            current_time = time.time()

            # Draw UI panel at the top
            ui_height = 120
            cv2.rectangle(frame, (0, 0), (width, ui_height), (40, 40, 40), -1)
            
            # Draw buttons
            pause_text = "RESUME" if state['paused'] else "PAUSE"
            pause_color = (0, 150, 0) if state['paused'] else (0, 0, 150)
            pause_button = draw_button(frame, pause_text, 10, 10, 80, 30, pause_color)
            
            sensitivity_up = draw_button(frame, "+", 100, 10, 30, 30, (0, 100, 0))
            sensitivity_down = draw_button(frame, "-", 140, 10, 30, 30, (100, 0, 0))
            
            # Set mouse callback with button parameters
            cv2.setMouseCallback(window_name, mouse_callback, (pause_button, sensitivity_up, sensitivity_down, state))
            
            # Display status information
            status_y = 55
            cv2.putText(frame, f"Drowsiness Score: {drowsiness_score}/{state['drowsiness_threshold']}", 
                       (10, status_y), font_small, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f"Absence Counter: {absence_counter}/{state['absence_threshold']}", 
                       (10, status_y + 20), font_small, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f"Status: {'PAUSED' if state['paused'] else 'MONITORING'}", 
                       (10, status_y + 40), font_small, 0.6, (255, 255, 0) if state['paused'] else (0, 255, 0), 1, cv2.LINE_AA)

            if not state['paused']:
                # Convert frame to grayscale for detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces and eyes
                faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
                left_eye = leye.detectMultiScale(gray)
                right_eye = reye.detectMultiScale(gray)

                # Draw detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
                    cv2.putText(frame, 'Face', (x, y-10), font_small, 0.5, (255, 255, 0), 1)

                # Check if eyes are present
                eyes_detected = len(left_eye) > 0 or len(right_eye) > 0
                
                if len(faces) > 0 and eyes_detected:
                    # Reset absence counter when eyes are detected
                    absence_counter = max(0, absence_counter - 2)
                    
                    if use_ml and model is not None:
                        # Use ML model for drowsiness detection
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
                            cv2.putText(frame, 'R', (x, y-5), font_small, 0.5, (255, 0, 0), 1)
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
                            cv2.putText(frame, 'L', (x, y-5), font_small, 0.5, (0, 255, 0), 1)
                            break

                        # Determine eye states
                        left_closed = False
                        right_closed = False
                        
                        try:
                            if len(lpred) > 0:
                                if hasattr(lpred[0], '__len__') and len(lpred[0]) > 1:
                                    left_closed = lpred[0][0] > lpred[0][1]
                                else:
                                    left_closed = float(lpred[0]) > 0.5
                        except:
                            left_closed = False
                            
                        try:
                            if len(rpred) > 0:
                                if hasattr(rpred[0], '__len__') and len(rpred[0]) > 1:
                                    right_closed = rpred[0][0] > rpred[0][1]
                                else:
                                    right_closed = float(rpred[0]) > 0.5
                        except:
                            right_closed = False

                        # Update drowsiness score
                        if left_closed or right_closed:
                            drowsiness_score += SENSITIVITY
                            eye_status = "Eyes Closed (AI)"
                            status_color = (0, 0, 255)
                        else:
                            drowsiness_score = max(0, drowsiness_score - SENSITIVITY)
                            eye_status = "Eyes Open (AI)"
                            status_color = (0, 255, 0)
                    else:
                        # Simple detection without ML
                        expected_eyes = len(faces) * 2
                        detected_eyes = len(left_eye) + len(right_eye)
                        
                        if detected_eyes < expected_eyes * 0.7:
                            drowsiness_score += SENSITIVITY
                            eye_status = "Possible Sleepiness"
                            status_color = (0, 165, 255)
                        else:
                            drowsiness_score = max(0, drowsiness_score - SENSITIVITY)
                            eye_status = "Eyes Detected"
                            status_color = (0, 255, 0)

                        # Draw detected eyes
                        for (x, y, w, h) in right_eye:
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                            cv2.putText(frame, 'R', (x, y-5), font_small, 0.5, (255, 0, 0), 1)
                        for (x, y, w, h) in left_eye:
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                            cv2.putText(frame, 'L', (x, y-5), font_small, 0.5, (0, 255, 0), 1)

                    # Display eye status
                    cv2.putText(frame, eye_status, (10, height - 40), font_small, 0.6, status_color, 1, cv2.LINE_AA)

                else:
                    # No face detected or no eyes detected
                    absence_counter += 1
                    eye_status = "Eyes Not Detected!"
                    status_color = (0, 0, 255)
                    
                    # Gradually reduce drowsiness score when no eyes detected
                    drowsiness_score = max(0, drowsiness_score - 0.5)
                    
                    # Display warning
                    cv2.putText(frame, eye_status, (10, height - 40), font_small, 0.6, status_color, 1, cv2.LINE_AA)
                    if len(faces) == 0:
                        cv2.putText(frame, "No Face Detected!", (10, height - 60), font_small, 0.6, (255, 0, 0), 1, cv2.LINE_AA)

                # Check for alerts (only if alarm cooldown has passed)
                should_alarm = current_time - last_alarm_time > alarm_cooldown

                # Check for drowsiness (eyes closed)
                if drowsiness_score >= state['drowsiness_threshold'] and should_alarm:
                    cv2.putText(frame, "DROWSINESS DETECTED!", (50, 200), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
                    cv2.putText(frame, "WAKE UP!", (50, 250), font, 1.5, (0, 0, 255), 4, cv2.LINE_AA)
                    
                    if drowsy_sound:
                        try:
                            drowsy_sound.play()
                            last_alarm_time = current_time
                        except:
                            pass

                    # Create red border
                    cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), 10)

                # Check for eye absence (looking away or sleeping)
                elif absence_counter >= state['absence_threshold'] and should_alarm:
                    cv2.putText(frame, "EYES NOT DETECTED!", (50, 200), font, 1.2, (255, 0, 0), 3, cv2.LINE_AA)
                    cv2.putText(frame, "LOOK AT CAMERA!", (50, 250), font, 1.2, (255, 0, 0), 3, cv2.LINE_AA)
                    
                    if absence_sound:
                        try:
                            absence_sound.play()
                            last_alarm_time = current_time
                        except:
                            pass

                    # Create blue border for absence detection
                    cv2.rectangle(frame, (0, 0), (width, height), (255, 0, 0), 8)

                # Warning levels
                elif drowsiness_score >= state['drowsiness_threshold'] * 0.7:
                    cv2.putText(frame, "Getting Sleepy...", (50, 200), font, 1, (0, 165, 255), 2, cv2.LINE_AA)
                elif absence_counter >= state['absence_threshold'] * 0.7:
                    cv2.putText(frame, "Eyes Missing...", (50, 200), font, 1, (255, 165, 0), 2, cv2.LINE_AA)

            else:
                # Paused state
                cv2.putText(frame, "DETECTION PAUSED", (width//2 - 150, height//2), font, 1.5, (255, 255, 0), 3, cv2.LINE_AA)
                cv2.putText(frame, "Click RESUME to continue", (width//2 - 120, height//2 + 50), font_small, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            # Always display current settings
            cv2.putText(frame, f"Absence Sensitivity: {state['absence_threshold']}", 
                       (width - 250, 30), font_small, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Display the frame
            cv2.imshow(window_name, frame)

            # Exit on 'q' key press
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):  # Spacebar to pause/resume
                state['paused'] = not state['paused']

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
    # Check if required files exist
    required_files = [
        'haar cascade files/haarcascade_frontalface_alt.xml',
        'haar cascade files/haarcascade_lefteye_2splits.xml',
        'haar cascade files/haarcascade_righteye_2splits.xml'
    ]
    
    # Check for alarm files
    alarm_files = ['alarm2.wav', 'TFALARM.WAV']
    alarm_found = any(os.path.exists(alarm) for alarm in alarm_files)
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if not alarm_found:
        print("⚠ Warning: No alarm files found. The system will work but without sound alerts.")
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all files are in the correct location.")
    else:
        print("✅ All required files found")
        main()
