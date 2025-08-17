
# 🛌 Student Sleep Detection System - User Guide (a.k.a. "Stay Awake, Genius!")

## 🎯 What This System Does

The **Student Sleep Detection System** is your AI-powered buddy that makes sure you don’t face-plant into your books while “studying” (aka staring at the screen until your eyes betray you).

How it works: your webcam plays detective, keeping an eye on your eyes 👀. If it suspects you’re nodding off into dreamland, it goes full drama mode:

* 🚨 Blasts an alarm (`alarm2.wav`) — yes, loud enough to make your neighbor question their life choices.  
* 🔴 Flashes a big red border around the screen — because subtlety is overrated.  
* 📊 Shows a **drowsiness score** climbing like your sleep debt before finals.  

Basically: It’s like having an overly concerned friend who yells “WAKE UP!” the moment you yawn too long.  

---

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

---

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

---

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

---

## 📊 Understanding the Display

Here’s what the system whispers to you on-screen:

* **Drowsiness Score**: Like your GPA, except it goes *up* when things get worse.  
* **Status**: Open/Closed eyes (your new live stream).  
* **Eye Count**: L = left, R = right. (Two eyes = good, one eye = pirate mode 🏴‍☠️)  
* **Face Detection**: Yellow boxes proving the system knows you exist.  

---

## ⚙️ How It Works (a.k.a. "Why it Feels Smarter Than You at 3 AM")

1. **Face Detection** 🧑 – Haar cascades sniff out your face.  
2. **Eye Detection** 👀 – Specialized classifiers track your left and right eyes separately.  
3. **AI Classification** 🧠 – CNN says: open or closed.  
4. **Drowsiness Scoring** 📈 – Score rises with closed eyes, drops with open eyes.  
5. **Alert System** 🔔 – Audio alarm + flashing border + text.  

---

## 🔧 Troubleshooting

**Common Issues (and your survival guide):**

1. **Model loading error** – Don’t panic, the fixed version (`sleep_detection_fixed.py`) has your back.  
2. **Could not open webcam** – Zoom/Teams probably hogging it. Kick them off.  
3. **No face detected** – Light up the room and stop hiding.  
4. **False alarms** – Improve lighting, ditch reflective shades, hands off your face.  

**Pro Tips 🧙‍♂️**  
* Light the room like you’re filming a TikTok.  
* Camera at eye level (nostrils don’t need to star in your study vlog).  
* Sit steady — don’t headbang like you’re at a metal concert.  

---

## 🛠️ Customization

Want more drama or less? Adjust thresholds in the Python scripts:

* **Basic mode**: `threshold = 1` (jumps at every blink)  
* **Enhanced mode**: `DROWSINESS_THRESHOLD = 10` (chiller)  

---

## 📝 Files Created for You

* `test_system.py` – Diagnostic check  
* `sleep_detection.py` – Bare-bones edition  
* `enhanced_sleep_detection.py` – Extra vigilant  
* `sleep_detection_fixed.py` – Smart fallback system (recommended)  

---

## 💡 Tips for Best Results

* Bright, comfy study room.  
* No backlighting (unless you want horror vibes).  
* Hair out of your eyes (sorry, anime cosplayers).  
* Camera = eye level. Not forehead, not chin.  

---

## 🎯 Study Effectiveness

This system is basically your nagging parent in software form. It:  

* Keeps you alert.  
* Tracks your “oops-I-dozed” patterns.  
* Prevents you from drooling on your books.  
* Encourages real breaks when you’re actually exhausted.  

---

## 🏁 Stopping the System

* Hit **`q`** like you mean it.  
* Or just close the terminal.  
* Either way: alarms won’t haunt you after.  

---

```
.·:'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''':·.
: : ███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗███████╗ : :
: : ████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝ : :
: : ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ███████╗ : :
: : ██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚════██║ : :
: : ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗███████║ : :
: : ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝ : :
'·:............................................................................................:·'
```

# ✨ NEW FEATURES UPDATE (2025 Edition)

Because staying awake isn’t hard enough, we added more ways to catch you slacking.  
Introducing the **Enhanced Sleep Detection Features** — now with more sass, more smarts, and *yes*, more alarms.  

👉 Full guide: [Enhanced Sleep Detection Features Guide](https://github.com/samganguly/student-sleep-detection/blob/main/NEW_FEATURES_GUIDE.md)

---

## 🚀 What’s New?

* 👁 **Eye Absence Detection** — detects when your eyes are MIA (looking away, sneaky micro-nap, or just ducking the camera).  
* 🎛 **Interactive UI Controls** — pause/resume button + sensitivity tuning + real-time status.  
* 🔔 **Dual Alert System** —  
  - 🔴 Red border + alarm = classic “you’re snoozing.”  
  - 🔵 Blue border + alarm = “hello? where’d your eyes go?”  

---

## 📂 Updated Files in the Repo

* `sleep_detection.py` → updated with **eye absence detection**.  
* `enhanced_sleep_detection_with_absence.py` → ✨ new full-featured version with UI buttons, adjustable sensitivity, dual alerts.  
* `sleep_detection_fixed.py` → still your safety net if models misbehave.  

Run the super-enhanced version:  
```powershell
python enhanced_sleep_detection_with_absence.py
```

---

## 📊 Comparison Table (Because Students Love Tables)

| Feature                        | `sleep_detection.py` | `enhanced_sleep_detection_with_absence.py` | `sleep_detection_fixed.py` |
|--------------------------------|-----------------------|---------------------------------------------|-----------------------------|
| Basic drowsiness detection     | ✅                   | ✅                                          | ✅                         |
| Eye absence detection          | ✅                   | ✅                                          | ❌                         |
| Pause/Resume button            | ❌                   | ✅                                          | ❌                         |
| Sensitivity controls           | ❌                   | ✅                                          | ❌                         |
| Advanced UI                    | ❌                   | ✅                                          | ❌                         |
| Model compatibility fixes      | ❌                   | ✅                                          | ✅                         |
| Dual alarm sounds              | ❌                   | ✅                                          | ❌                         |

---

## 💡 Why You’ll Love the New Features

* **More comprehensive**: catches sleeping *and* inattention.  
* **User control**: pause for real breaks, tweak sensitivity like a DJ.  
* **Better feedback**: red vs blue alerts = crystal clear.  
* **Professional**: now you can pretend this is for “work from home focus” instead of cramming.  

---

## 🎯 Final Word

So whether you’re:  
- A student pulling all-nighters ☕📚  
- Someone “listening” to Zoom lectures 👀  
- Or just trying not to embarrass yourself on a Teams call 💼  

…the enhanced version has your back.  

👉 Try out [`enhanced_sleep_detection_with_absence.py`](https://github.com/samganguly/student-sleep-detection/blob/main/enhanced_sleep_detection_with_absence.py) for the **best experience**.  

**Stay awake, stay focused, and may your GPA rise as fast as your drowsiness score!** 🚀  
