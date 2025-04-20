import cv2

def initialize_tracker(frame):
    bbox = cv2.selectROI("Select Person", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Person")

    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, bbox)
    return tracker, bbox