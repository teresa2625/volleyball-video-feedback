# 🕺 Pose Tracker with Feedback

A Python-based video processor that lets you select a person in a video, tracks them using a bounding box, detects body poses with MediaPipe, and gives basic feedback based on joint angles like knee and elbow.

---

## 📦 Features

- Person selection via bounding box
- Pose detection using [MediaPipe](https://google.github.io/mediapipe/)
- Tracking via OpenCV's CSRT tracker
- Real-time feedback based on knee and elbow angles
- Output video with overlaid poses
- Feedback CSV file export per frame

---

## 🧰 Requirements

Make sure you have Python 3.7+ and install the dependencies:

```bash
pip install opencv-python mediapipe
```

---

## 🚀 How to Run

```bash
python main.py <input_video_path> <output_video_path>
```

Example:

```bash
python main.py input.mp4 output.avi
```

---

## 📄 Output

- A new video (`.avi`) with pose overlays and bounding box tracking
- A CSV file (`output_feedback.csv`) with:
  - Frame number
  - Knee angle
  - Elbow angle
  - Feedback message

---

## 🧠 How It Works

1. You select a person by drawing a box on the first frame.
2. The CSRT tracker follows the selected person.
3. For each frame:
   - Pose landmarks are detected.
   - Angles are estimated (currently dummy values).
   - Feedback is written to a CSV.

---

## 📝 Notes

- Knee and elbow angle calculations are placeholders. You can plug in your own logic in:
  - `calculate_knee_angle()`
  - `calculate_elbow_angle()`
- The video is rotated 90° counterclockwise for processing.

---

## 🔧 File Structure

```
project/
│
├── main.py                # Main logic
├── input.mp4              # Your input video (not included)
├── output.avi             # Resulting video
└── output_feedback.csv    # CSV feedback (generated after processing)
```

---

## 🧑‍💻 Todo

- ✅ Person tracking with OpenCV
- ✅ Pose detection using MediaPipe
- ✅ Basic feedback logic
- ❌ Real knee/elbow angle calculation
- ❌ GUI for easier interaction

---

## 🐛 Issues

If you run into issues, feel free to open an issue or pull request. Contributions are welcome!

---
