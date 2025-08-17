# Enhanced Sleep Detection Features Guide

##  New Features Added

### 1. **Eye Absence Detection**
- **What it does**: Detects when your eyes are not visible in the camera
- **Why it's useful**: Catches when you're looking away, dozing with eyes open, or have moved out of camera view
- **How it works**: Counts frames where no eyes are detected and triggers alarm after threshold

### 2. **Interactive UI Controls**
- **Pause/Resume Button**: Click to pause/resume detection
- **Sensitivity Controls**: +/- buttons to adjust absence detection sensitivity
- **Real-time Status**: Shows current monitoring state and scores

### 3. **Dual Alert System**
- **Red Border + Alarm**: Eyes closed (drowsiness)
- **Blue Border + Alarm**: Eyes not detected (absence/inattention)

## 📁 File Versions Available

### 1. `sleep_detection.py` (Updated)
- **Original version** with eye absence detection added
- Simple interface
- Dual detection: drowsiness + absence

### 2. `enhanced_sleep_detection_with_absence.py` (NEW)
- **Full-featured version** with advanced UI
- Clickable pause/resume button
- Adjustable sensitivity controls
- Better visual feedback
- Two different alarm sounds (if available)

### 3. `sleep_detection_fixed.py`
- **Compatibility version** for model loading issues
- Fallback detection if AI models fail

##  How to Use the New Features

### Running the Enhanced Version
```powershell
python enhanced_sleep_detection_with_absence.py
```

### UI Controls
1. **Pause Button**: 
   - Click "PAUSE" to stop monitoring
   - Click "RESUME" to restart monitoring
   - Useful during breaks or when talking to someone

2. **Sensitivity Buttons**:
   - Click "+" to increase sensitivity (lower threshold)
   - Click "-" to decrease sensitivity (higher threshold)
   - Adjusts how quickly eye absence is detected

3. **Keyboard Shortcuts**:
   - Press `Spacebar` to pause/resume
   - Press `q` to quit

### Detection Types

#### 🔴 Drowsiness Detection (Red Alert)
- **Triggers when**: Eyes are detected as closed for sustained period
- **Visual**: Red flashing border
- **Audio**: Primary alarm sound (`alarm2.wav`)
- **Message**: "DROWSINESS DETECTED! WAKE UP!"

#### 🔵 Eye Absence Detection (Blue Alert)
- **Triggers when**: Eyes not detected for sustained period
- **Visual**: Blue solid border
- **Audio**: Secondary alarm sound (`TFALARM.WAV` or same alarm)
- **Message**: "EYES NOT DETECTED! LOOK AT CAMERA!"

### Status Display
The UI shows:
- **Drowsiness Score**: Increases with closed eyes
- **Absence Counter**: Increases when eyes not detected
- **Current Status**: MONITORING or PAUSED
- **Detection Mode**: Shows if using AI or basic detection

## 🔧 Customizable Settings

### Thresholds (in code)
```python
DROWSINESS_THRESHOLD = 15    # Points for drowsiness alarm
ABSENCE_THRESHOLD = 30       # Frames for absence alarm
```

### Sensitivity Levels
- **High Sensitivity**: Lower thresholds (5-15 frames)
- **Medium Sensitivity**: Default thresholds (20-30 frames)
- **Low Sensitivity**: Higher thresholds (40+ frames)

## 💡 Use Cases

### 1. **Study Sessions**
- Detects both falling asleep AND looking away from study material
- Helps maintain focus on books/screen

### 2. **Online Classes**
- Ensures you're paying attention to the camera/screen
- Alerts if you zone out or look elsewhere

### 3. **Work from Home**
- Maintains alertness during video calls
- Prevents appearing inattentive during meetings

### 4. **Break Management**
- Use pause button when taking legitimate breaks
- Resume when ready to continue focused work

## 🎯 Optimal Setup

### Camera Position
- **Distance**: 2-3 feet from your face
- **Height**: At eye level
- **Angle**: Straight on, not looking up or down

### Lighting
- **Avoid**: Bright lights behind you (backlighting)
- **Prefer**: Even lighting on your face
- **Best**: Natural light from side or front

### Environment
- **Stable position**: Avoid moving around too much
- **Clear view**: Remove objects that might block eye view
- **Glasses**: Remove reflective glasses if causing detection issues

## 🚨 Alert Meanings

| Alert Type | Visual | Audio | Meaning | Action |
|------------|--------|-------|---------|---------|
| Red Border | Flashing red frame | Primary alarm | Eyes closed (drowsy) | Wake up! |
| Blue Border | Solid blue frame | Secondary alarm | Eyes not visible | Look at camera |
| Orange Text | "Getting Sleepy..." | None | Early warning | Sit up straight |
| Yellow Text | "Eyes Missing..." | None | Early absence warning | Adjust position |

## 🔄 Comparison of Files

| Feature | sleep_detection.py | enhanced_...absence.py | sleep_detection_fixed.py |
|---------|-------------------|----------------------|-------------------------|
| Basic drowsiness detection | ✅ | ✅ | ✅ |
| Eye absence detection | ✅ | ✅ | ❌ |
| Pause/Resume button | ❌ | ✅ | ❌ |
| Sensitivity controls | ❌ | ✅ | ❌ |
| Advanced UI | ❌ | ✅ | ❌ |
| Model compatibility fixes | ❌ | ✅ | ✅ |
| Dual alarm sounds | ❌ | ✅ | ❌ |

## Benefits of New Features

1. **More Comprehensive**: Catches both sleeping AND inattention
2. **User Control**: Pause when needed, adjust sensitivity
3. **Better Feedback**: Clear visual indicators of what's happening
4. **Flexible**: Works for different use cases and preferences
5. **Professional**: Suitable for work/study environments

**Recommendation**: Use `enhanced_sleep_detection_with_absence.py` for the best experience!
