import cv2
import mediapipe as mp
import os
import csv
import math

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def process_video(input_path, output_path):
    print(f"🔄 Starting processing for: {input_path}")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("❌ Failed to open input video.")
        return

    success, first_frame = cap.read()
    if not success:
        print("❌ Failed to read first frame.")
        return

    first_frame = cv2.rotate(first_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    bbox = cv2.selectROI("Select Person", first_frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Person")

    if bbox == (0, 0, 0, 0):
        print("❌ No region selected.")
        return

    print(f"📦 Selected bounding box: {bbox}")

    tracker = cv2.TrackerCSRT_create()
    tracker.init(first_frame, bbox)

    height, width, _ = first_frame.shape
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_interval = int(fps * 0.5)

    if not output_path.endswith(".mp4"):
        output_path = os.path.splitext(output_path)[0] + ".mp4"

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not out.isOpened():
        raise ValueError("❌ Failed to initialize VideoWriter.")

    pose = mp_pose.Pose(static_image_mode=False)
    frame_count = 0

    csv_filename = os.path.splitext(output_path)[0] + "_feedback.csv"
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Time (s)', 'Knee Angle', 'Elbow Angle', 'Feedback'])

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        while True:
            ret, frame = cap.read()
            if not ret:
                print("📥 No more frames to read. Exiting.")
                break

            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            success, bbox = tracker.update(frame)
            if success:
                x, y, w, h = map(int, bbox)
                roi = frame[y:y+h, x:x+w]

                image_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                results = pose.process(image_rgb)

                left_knee_angle = right_knee_angle = None
                left_elbow_angle = right_elbow_angle = None
                feedback = []

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(roi, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    landmarks = results.pose_landmarks.landmark

                    def get_coords(idx):
                        lm = landmarks[idx]
                        return (lm.x, lm.y)

                    try:
                        left_knee_angle = calculate_angle(
                            get_coords(mp_pose.PoseLandmark.LEFT_HIP),
                            get_coords(mp_pose.PoseLandmark.LEFT_KNEE),
                            get_coords(mp_pose.PoseLandmark.LEFT_ANKLE)
                        )
                    except: pass

                    try:
                        right_knee_angle = calculate_angle(
                            get_coords(mp_pose.PoseLandmark.RIGHT_HIP),
                            get_coords(mp_pose.PoseLandmark.RIGHT_KNEE),
                            get_coords(mp_pose.PoseLandmark.RIGHT_ANKLE)
                        )
                    except: pass

                    try:
                        left_elbow_angle = calculate_angle(
                            get_coords(mp_pose.PoseLandmark.LEFT_SHOULDER),
                            get_coords(mp_pose.PoseLandmark.LEFT_ELBOW),
                            get_coords(mp_pose.PoseLandmark.LEFT_WRIST)
                        )
                    except: pass

                    try:
                        right_elbow_angle = calculate_angle(
                            get_coords(mp_pose.PoseLandmark.RIGHT_SHOULDER),
                            get_coords(mp_pose.PoseLandmark.RIGHT_ELBOW),
                            get_coords(mp_pose.PoseLandmark.RIGHT_WRIST)
                        )
                    except: pass

                    feedback.extend(provide_feedback(
                        left_knee_angle, right_knee_angle,
                        left_elbow_angle, right_elbow_angle
                    ))

                frame[y:y+h, x:x+w] = roi
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                timestamp = round(frame_count / fps, 2)
                csv_writer.writerow([
                    timestamp,
                    f"{left_knee_angle:.1f}" if left_knee_angle else "",
                    f"{right_knee_angle:.1f}" if right_knee_angle else "",
                    f"{left_elbow_angle:.1f}" if left_elbow_angle else "",
                    f"{right_elbow_angle:.1f}" if right_elbow_angle else "",
                    "; ".join(feedback)
                ])

            else:
                print(f"⚠️ Tracking lost at frame {frame_count}.")

            out.write(frame)
            frame_count += frame_interval

    print(f"✅ Done. Total frames processed: {frame_count}")
    print(f"🎬 Output saved to: {output_path}")

    cap.release()
    out.release()

def calculate_angle(a, b, c):
    # a, b, c are (x, y)
    def distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    ab = distance(a, b)
    bc = distance(b, c)
    ac = distance(a, c)

    if ab * bc == 0:
        return None

    angle = math.acos((ab**2 + bc**2 - ac**2) / (2 * ab * bc))
    return math.degrees(angle)

def provide_feedback(l_knee, r_knee, l_elbow, r_elbow):
    feedback = []

    for side, angle in [('Left knee', l_knee), ('Right knee', r_knee)]:
        if angle is None:
            feedback.append(f"{side} not visible")
        elif angle < 90:
            feedback.append(f"{side} too bent")
        elif angle > 160:
            feedback.append(f"{side} too straight")
        else:
            feedback.append(f"{side} good")

    for side, angle in [('Left elbow', l_elbow), ('Right elbow', r_elbow)]:
        if angle is None:
            feedback.append(f"{side} not visible")
        elif angle < 90:
            feedback.append(f"{side} too bent")
        elif angle > 160:
            feedback.append(f"{side} too straight")
        else:
            feedback.append(f"{side} good")

    return feedback
