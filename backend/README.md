# 🕺 Pose Tracker with Feedback

A Python-based video processor that lets you select a person in a video, tracks them using a bounding box, detects body poses with MediaPipe, and gives basic feedback based on joint angles like knee and elbow.

## 📦 Features

- Person selection via bounding box
- Pose detection using [MediaPipe](https://google.github.io/mediapipe/)
- Tracking via OpenCV's CSRT tracker
- Real-time feedback based on knee and elbow angles
- Output video with overlaid poses
- Feedback CSV file export per frame

## 🧰 Requirements

Make sure you have Python 3.7+ and install the dependencies:

## Running the Backend

1. Clone the repository:

```
git clone https://github.com/teresa2625/volleyball-video-feedback
cd backend
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Start the backend server:

```bash
uvicorn app:app --reload
```

## 📄 Output

- A new video (`.avi`) with pose overlays and bounding box tracking
- A CSV file (`output_feedback.csv`) with:
  - Time number
  - Knee angle
  - Elbow angle
  - Feedback message

## 🧠 How It Works

1. You select a person by drawing a box on the first frame.
2. The CSRT tracker follows the selected person.
3. For each frame:
   - Pose landmarks are detected.
   - Angles are estimated (currently dummy values).
   - Feedback is written to a CSV.

## 📝 Notes

- Knee and elbow angle calculations are placeholders. You can plug in your own logic in:
  - `calculate_knee_angle()`
  - `calculate_elbow_angle()`
- The video is rotated 90° counterclockwise for processing.

## 🔧 File Structure

```
backend/
├── app.py
├── video_process/
│   ├── processor.py      # main video logic
│   └── tracker.py        # tracking and ROI logic
├── calculations/
│   ├── angle.py          # angle calculations
│   ├── jump.py           # jump detection
│   └── spike.py          # spike analysis
├── input.mp4             # Your input video (not included)
├── output.mp4            # Resulting video (generated after processing)
├── output_feedback.csv   # CSV feedback (generated after processing)
└── requirements.txt      # Dependencies
```

## 🧑‍💻 Todo

- ✅ Person tracking with OpenCV
- ✅ Pose detection using MediaPipe
- ✅ Basic feedback logic
- ❌ Real knee/elbow angle calculation
- ❌ GUI for easier interaction
