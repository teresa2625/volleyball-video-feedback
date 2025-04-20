def detect_jump(is_jumping, previous_hip_y, hip_y, jump_start_time, timestamp, height):
    jump_threshold = 0.05
    min_jump_height_px = 10

    jump_event = None
    if previous_hip_y is not None:
        jump_height = previous_hip_y - hip_y

        if not is_jumping and jump_height > jump_threshold:
            is_jumping = True
            jump_start_time = timestamp
            jump_pixels = int(jump_height * height)
            feedback = f"At {timestamp}s, you jumped {jump_pixels}px. Try jumping at least {min_jump_height_px}px higher."
            jump_event = (timestamp, "Jump", feedback)

        elif is_jumping and jump_height < 0.01:
            is_jumping = False

    return is_jumping, jump_start_time, jump_event