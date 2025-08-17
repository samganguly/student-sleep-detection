"""
Test script to check if all components are working
"""

import os
import cv2
import numpy as np

def test_system():
    print("🔍 Testing Student Sleep Detection System Components...")
    print("=" * 60)
    
    # Test 1: Check required files
    print("📁 Checking required files...")
    required_files = {
        'alarm2.wav': 'Alarm sound file',
        'haar cascade files/haarcascade_frontalface_alt.xml': 'Face detection model',
        'haar cascade files/haarcascade_lefteye_2splits.xml': 'Left eye detection model',
        'haar cascade files/haarcascade_righteye_2splits.xml': 'Right eye detection model',
        'models/cnn.h5': 'Original CNN model',
        'models/cnn_eye_classification.h5': 'Enhanced CNN model'
    }
    
    missing_files = []
    for file, description in required_files.items():
        if os.path.exists(file):
            print(f"✅ {description}: Found")
        else:
            print(f"❌ {description}: Missing ({file})")
            missing_files.append(file)
    
    # Test 2: Check webcam
    print(f"\n📷 Testing webcam...")
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ Webcam working - Frame size: {frame.shape}")
            else:
                print("❌ Webcam not returning frames")
            cap.release()
        else:
            print("❌ Could not open webcam")
    except Exception as e:
        print(f"❌ Webcam error: {e}")
    
    # Test 3: Check Python packages
    print(f"\n📦 Testing Python packages...")
    packages = {
        'cv2': 'OpenCV',
        'tensorflow': 'TensorFlow',
        'keras': 'Keras',
        'pygame': 'Pygame',
        'numpy': 'NumPy'
    }
    
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✅ {name}: Installed")
        except ImportError:
            print(f"❌ {name}: Not installed")
    
    # Test 4: Check if models can be loaded
    print(f"\n🧠 Testing CNN models...")
    try:
        from keras.models import load_model
        
        if os.path.exists('models/cnn.h5'):
            model = load_model('models/cnn.h5')
            print(f"✅ Original CNN model: Loaded successfully")
        else:
            print(f"❌ Original CNN model: File not found")
            
        if os.path.exists('models/cnn_eye_classification.h5'):
            model = load_model('models/cnn_eye_classification.h5')
            print(f"✅ Enhanced CNN model: Loaded successfully")
        else:
            print(f"❌ Enhanced CNN model: File not found")
            
    except Exception as e:
        print(f"❌ Model loading error: {e}")
    
    # Test 5: Check Haar cascades
    print(f"\n👁 Testing Haar cascade classifiers...")
    cascades = {
        'haar cascade files/haarcascade_frontalface_alt.xml': 'Face detector',
        'haar cascade files/haarcascade_lefteye_2splits.xml': 'Left eye detector',
        'haar cascade files/haarcascade_righteye_2splits.xml': 'Right eye detector'
    }
    
    for file, name in cascades.items():
        try:
            if os.path.exists(file):
                cascade = cv2.CascadeClassifier(file)
                if not cascade.empty():
                    print(f"✅ {name}: Loaded successfully")
                else:
                    print(f"❌ {name}: Failed to load")
            else:
                print(f"❌ {name}: File not found")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
    
    # Summary
    print(f"\n📋 Summary:")
    if len(missing_files) == 0:
        print("🎉 All components are ready! You can run the sleep detection system.")
        print(f"\n🚀 To start detection, run:")
        print(f"   python sleep_detection.py          (Basic version)")
        print(f"   python enhanced_sleep_detection.py (Enhanced version)")
    else:
        print(f"⚠ {len(missing_files)} files are missing. Please ensure all required files are present.")

if __name__ == "__main__":
    test_system()
