from calculations.angle import calculate_angle

def analyze_spike(side, get_coords, timestamp, is_jumping, events):
    import mediapipe as mp
    pose = mp.solutions.pose.PoseLandmark

    try:
        if side == "LEFT":
            shoulder = pose.LEFT_SHOULDER
            elbow = pose.LEFT_ELBOW
            wrist = pose.LEFT_WRIST
        else:
            shoulder = pose.RIGHT_SHOULDER
            elbow = pose.RIGHT_ELBOW
            wrist = pose.RIGHT_WRIST

        angle = calculate_angle(
            get_coords(shoulder),
            get_coords(elbow),
            get_coords(wrist)
        )
        wrist_y = get_coords(wrist)[1]
        shoulder_y = get_coords(shoulder)[1]

        if is_jumping and wrist_y < shoulder_y and angle and angle > 130:
            feedback = f"At {timestamp}s, during your spike, your {side.lower()} elbow angle was {int(angle)}°. Try to keep it below 130°."
            events.append((timestamp, "Spike", feedback))
    except:
        pass