import cv2

def initialize_tracker(frame, bbox):

    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, bbox)
    return tracker