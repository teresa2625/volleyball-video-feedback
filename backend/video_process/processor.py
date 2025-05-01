import cv2
import mediapipe as mp
import os
import csv
import logging
import numpy as np
import subprocess
import json

from video_process.tracker import initialize_tracker
from calculations.jump import detect_jump
from calculations.spike import analyze_spike
from calculations.angle import calculate_angle

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

logger = logging.getLogger(__name__)

def rotate_frame(frame, angle):
    if angle == 90:
        return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return frame

def get_video_rotation(path):
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-show_entries', 'stream_tags=rotate,side_data_list', '-of', 'json', path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    metadata = json.loads(result.stdout)
    

    try:
        rotation = metadata['streams'][0]['tags']['rotate']
        return int(rotation)
    except KeyError:
        try:
            side_data = metadata['streams'][0]['side_data_list']
            if side_data:
                return 90
        except (KeyError, IndexError):
            pass
    return 0

def process_video(input_path, output_path, bbox):
    cap = cv2.VideoCapture(input_path)
    rotation = get_video_rotation(input_path)
    if not cap.isOpened():
        return
    success, first_frame = cap.read()
    if not success:
        logger.info("❌ Failed to read first frame.")
        return
    
    if isinstance(bbox, dict):
        bbox = (
            int(bbox["x"]),
            int(bbox["y"]),
            int(bbox["w"]),
            int(bbox["h"]),
        )
    first_frame = rotate_frame(first_frame, rotation)
    tracker = initialize_tracker(first_frame, bbox)
    if bbox == (0, 0, 0, 0):
        logger.info("❌ No region selected.")
        return
    height, width, _ = first_frame.shape
    original_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    fps = original_fps / 2  # 🐢 Slower output video

    if not output_path.endswith(".mp4"):
        output_path = os.path.splitext(output_path)[0] + ".mp4"

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not out.isOpened():
        raise ValueError("❌ Failed to initialize VideoWriter.")

    pose = mp_pose.Pose(static_image_mode=False)
    frame_count = 0
    events = []

    previous_hip_y = None
    is_jumping = False
    jump_start_time = None

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    while True:
        ret, frame = cap.read()
        if not ret:
            logger.info("📥 No more frames to read. Exiting.")
            break

        frame = rotate_frame(frame, rotation)
        success, bbox = tracker.update(frame)

        if success:
            x, y, w, h = map(int, bbox)
            roi = frame[y:y+h, x:x+w]
            image_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(roi, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                landmarks = results.pose_landmarks.landmark

                def get_coords(idx):
                    lm = landmarks[idx]
                    return (lm.x, lm.y)

                try:
                    left_hip = get_coords(mp_pose.PoseLandmark.LEFT_HIP)
                    right_hip = get_coords(mp_pose.PoseLandmark.RIGHT_HIP)
                    hip_y = (left_hip[1] + right_hip[1]) / 2

                    timestamp = round(frame_count / fps, 2)

                    (
                        is_jumping,
                        jump_start_time,
                        jump_event
                    ) = detect_jump(
                        is_jumping, previous_hip_y, hip_y, jump_start_time, timestamp, h
                    )
                    if jump_event:
                        events.append(jump_event)

                    previous_hip_y = hip_y

                    for side in ["LEFT", "RIGHT"]:
                        analyze_spike(
                            side, get_coords, timestamp, is_jumping, events
                        )

                except Exception as e:
                    logger.info(f"⚠️ Landmark processing error: {e}")

            frame[y:y+h, x:x+w] = roi
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        else:
            logger.info(f"⚠️ Tracking lost at frame {frame_count}.")

        out.write(frame)
        frame_count += 1

    logger.info(f"✅ Done. Total frames processed: {frame_count}")
    logger.info(f"🎬 Output saved to: {output_path}")

    cap.release()
    out.release()

    csv_filename = os.path.splitext(output_path)[0] + "_feedback.csv"
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Time (s)", "Event", "Feedback"])
        for event in events:
            csv_writer.writerow(event)

    logger.info(f"📝 Feedback saved to: {csv_filename}")