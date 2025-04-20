import math

def calculate_angle(a, b, c):
    def distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    ab = distance(a, b)
    bc = distance(b, c)
    ac = distance(a, c)

    if ab * bc == 0:
        return None

    angle = math.acos((ab**2 + bc**2 - ac**2) / (2 * ab * bc))
    return math.degrees(angle)