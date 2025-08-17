# 🛌 Student Sleep Detection System - User Guide (a.k.a. "Stay Awake, Genius!")

## 🎯 What This System Does

The **Student Sleep Detection System** is your AI-powered buddy that makes sure you don’t face-plant into your books while “studying” (aka staring at the screen until your eyes betray you).

How it works: your webcam plays detective, keeping an eye on your eyes 👀. If it suspects you’re nodding off into dreamland, it goes full drama mode:

* 🚨 Blasts an alarm (`alarm2.wav`) — yes, loud enough to make your neighbor question their life choices.
* 🔴 Flashes a big red border around the screen — because subtlety is overrated.
* 📊 Shows a **drowsiness score** climbing like your sleep debt before finals.

Basically: It’s like having an overly concerned friend who yells “WAKE UP!” the moment you yawn too long.


## 📁 Project Structure

Inside your magical **Student Falling Sleep Detection** folder, you’ll find a buffet of files and models. Here’s the lay of the land:

```
📂 Student Falling Sleep Detection/
├── 🎵 alarm2.wav                          # The not-so-gentle wake-up call
├── 📓 student sleeping detection.ipynb    # The OG notebook
├── 📓 model.ipynb                         # Where the brains are trained
├── 📂 models/
│   ├── 🧠 cnn.h5                         # Old-school CNN model
│   ├── 🧠 cnn_eye_classification.h5      # Eye-detection prodigy
│   └── 🧠 cnnCat2.h5                     # Another fancy model (because why not?)
├── 📂 haar cascade files/
│   ├── 👤 haarcascade_frontalface_alt.xml     # Finds your face, even on bad hair days
│   ├── 👁 haarcascade_lefteye_2splits.xml     # Left eye spy
│   └── 👁 haarcascade_righteye_2splits.xml    # Right eye spy
├── 📂 data/
│   ├── 📂 train/closed/                   # Pics of closed eyes (yes, they exist)
│   ├── 📂 train/open/                     # Pics of wide-awake eyes
│   └── 📂 valid/                          # Validation stash
└── 🐍 Python scripts
```


## 🚀 How to Run the Sleep Detection System

You’ve got options. Just like ordering coffee, you can go for **basic, strong, or extra fancy.**

### Method 1: Quick Test (Recommended ☕)

1. **Run a quick system check**

   ```powershell
   python test_system.py
   ```

   This ensures all the wires, models, and alarms are ready. Basically a dress rehearsal.

2. **Fire up the fixed system** (the one less likely to crash on you):

   ```powershell
   python sleep_detection_fixed.py
   ```

### Method 2: Alternative Flavors 🍦

* **Basic version (vanilla):**

  ```powershell
  python sleep_detection.py
  ```

* **Enhanced version (espresso shot):**

  ```powershell
  python enhanced_sleep_detection.py
  ```

### Method 3: The Jupyter Notebook Route 📓

If you’re feeling academic:

1. Open `student sleeping detection.ipynb` in VS Code
2. Run the cells one by one
3. Watch the magic unfold — bonus: you can peek inside the code like a curious cat 🐱


## 🎮 How to Use

1. Start one of the scripts (choose your adventure).
2. Sit in front of your webcam like you’re about to record a vlog.
3. Make sure your face is actually visible (no blankets, no hiding).
4. Yellow boxes = faces detected (yay!).
5. Green 🟢 box = left eye detected. Blue 🔵 box = right eye detected.
6. Keep an eye on your **drowsiness score** (pun intended). It climbs if you’re snoozing.
7. If it thinks you’re falling asleep:

   * 🚨 Alarm goes off
   * 🔴 Red flashing border (like your PC is screaming “CODE RED!”)
   * ⚠️ Giant “DROWSINESS DETECTED!” message.
8. Too much? Press **`q`** to quit gracefully.


## 📊 Understanding the Display

Here’s what the system whispers to you on-screen:

* **Drowsiness Score**: Like your GPA, except it goes *up* when things get worse.
* **Status**: Open/Closed eyes (your new live stream).
* **Eye Count**: L = left, R = right. (Two eyes = good, one eye = pirate mode 🏴‍☠️)
* **Face Detection**: Yellow boxes proving the system knows you exist.


## ⚙️ How It Works (a.k.a. "Why it Feels Smarter Than You at 3 AM")

1. **Face Detection** 🧑
   Haar cascades sniff out your face — even if you’re pulling an all-nighter.

2. **Eye Detection** 👀
   Specialized classifiers track your left and right eyes separately (no favoritism).

3. **AI Classification** 🧠
   CNN model takes a tiny 24x24 grayscale eye image and declares: **open** or **closed**. Like Tinder for your eyelids.

4. **Drowsiness Scoring** 📈

   * Closed eyes = score goes up.
   * Open eyes = score drops.
   * Hit the threshold = BOOM, alarm time.

5. **Alert System** 🔔

   * Audio alarm
   * Flashing border
   * Text warning
     Basically, a triple combo attack to scare you awake.


## 🔧 Troubleshooting

### Common Issues (and your survival guide):

1. **Model loading error**

   * Don’t panic. The fixed version will switch to plan B automatically.

2. **Could not open webcam**

   * Close Zoom, Teams, or whatever’s hogging your camera.

3. **No face detected**

   * Brighten the room.
   * Don’t sit 1 cm away from the camera.
   * Stop hiding like you’re in a witness protection program.

4. **False alarms**

   * Better lighting.
   * Don’t wear reflective shades.
   * Keep your hands away from your face (yes, we see you).

### Pro Tips 🧙‍♂️

* Light the room like you’re shooting a TikTok.
* Sit steady — don’t bob like you’re in a rock concert.
* Distance = 2–3 feet (not nose-to-screen).


## 🛠️ Customization

Want more drama or less? Adjust thresholds in the Python scripts:

* **Basic mode**: `threshold = 1` (jumps at every blink)
* **Enhanced mode**: `DROWSINESS_THRESHOLD = 10` (a little more chill)


## 📝 Files Created for You (a.k.a. Shortcuts for Lazy Geniuses)

* `test_system.py` – Diagnostic check
* `sleep_detection.py` – Bare-bones edition
* `enhanced_sleep_detection.py` – Extra vigilant
* `sleep_detection_fixed.py` – Smart fallback system (recommended)


## 💡 Tips for Best Results

* Use in a bright, comfy study room.
* No bright light *behind* you (unless you’re auditioning for a horror film).
* Remove shiny glasses.
* Tie back hair that covers your eyes (sorry, anime fans).
* Camera at eye level — not nostril level, please.


## 🎯 Study Effectiveness

This system is basically your nagging parent in software form. It:

* Keeps you alert.
* Tracks your “oops-I-dozed” patterns.
* Prevents you from drooling on your books.
* Encourages real breaks when you’re actually exhausted.

Remember: if the alarm keeps going off, that’s not the system’s fault. That’s your body begging for sleep. Don’t fight it. 😴


## 🏁 Stopping the System

* Hit **`q`** like you mean it.
* Or slam the terminal shut.
* Either way, the system will clean itself up (no zombie alarms left behind).


**Happy studying, you sleepless scholar! 📚✨**
And hey, if this system wakes you up more often than your morning coffee — mission accomplished. ☕

Do drop a Star✨ to this repo if this helped you get through your exam phase :D