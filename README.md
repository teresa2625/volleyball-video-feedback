# 🕺 Pose Tracker with Feedback

A Python-based video processor that lets you select a person in a video, tracks them using a bounding box, detects body poses with MediaPipe, and gives basic feedback based on joint angles like knee and elbow.

## Tech Stack

- **Frontend**: React + TypeScript + Axios
- **Backend**: Python + FastAPI + MediaPipe + OpenCV
- **CI/CD**: GitHub Actions
- **Infrastructure**: Terraform, AWS (optional for deployment)
- **Testing**:

## Features

- Upload a volleyball video through the web interface
- Backend processes the video:
  - Track player movements
  - Detect body landmarks
  - Calculate elbow and knee angles
  - Provide feedback based on posture
- Returns a processed video with visual feedback and a CSV report
- CSV includes time-based pose analysis (in seconds)

## Project Structure

volleyball-video-feedback/
├── backend/
│ │
│ ├── app.py
│ ├── video_utils.py # FastAPI server
│ ├── input.mp4 # Your input video (not included)
│ ├── output.avi # Resulting video (generated after processing)
│ ├── output_feedback.csv # CSV feedback (generated after processing)
| └── requirements.txt # Dependencies
├── frontend/
│ ├── src/
│ │ ├── App.tsx # Upload form + video preview
│ │ └── api.ts # Axios API calls
│ └── package.json
└── README.md

## Project Setup

### Prerequisites

Before running the project, ensure you have the following installed:

- Node.js (LTS version recommended)
- npm or Yarn (for managing dependencies)
- Make sure you have Python 3.7+ and install the dependencies

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

## Running the Frontend

Open a new terminal window and navigate to the frontend directory (if it's in a separate folder):

1. Clone the repository:

```
git clone https://github.com/teresa2625/volleyball-video-feedback
cd frontend
```

2. Install the frontend dependencies:

```
yarn install
```

3. Start the frontend development server:

```
yarn start
```

This will run the frontend server, and it will be available at http://localhost:3000 by default.

Now, you can access the application by navigating to http://localhost:3000 in your browser. The frontend will interact with the backend to process the video and generate feedback.

## TODO:
