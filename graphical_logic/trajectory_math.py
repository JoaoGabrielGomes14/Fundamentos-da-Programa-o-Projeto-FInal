import math
from graphics import Point

###build the trajectories for scenario 2
Points = list[tuple[float,float]] 

SIMULATION_X = 1.0
SIMULATION_Y = 2.0

RADIUS = 0.5

LOWER_CIRCLE_CENTER = (0.5,0.5)
UPPER_CIRCLE_CENTER = (0.5,1.5)

def line(start:tuple[float,float],end:tuple[float,float],number_points:int)->Points:
    line = []
    (x1,y1) , (x2,y2) = start,end

    for point in range(number_points+1):
        line.append(
            (x1 + (x2 - x1) * point / number_points, y1 + (y2 - y1) * point / number_points)
        )
    return line


def arc(center: tuple[float, float], radius: float,start_deg: float, end_deg: float, number_points: int) -> Points:
    
    cx, cy = center
    points: list[tuple [float,float]] = []

    for i in range(number_points + 1):
        angle = math.radians(start_deg + (end_deg - start_deg) * i / number_points)
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return points


def ring(number_points:int) -> Points:
    return (line((1, 0.5), (1, 1.5), number_points)[:-1]
            + arc(UPPER_CIRCLE_CENTER, RADIUS, 0, 180, number_points)[:-1]
            + line((0, 1.5), (0, 0.5), number_points)[:-1]
            + arc(LOWER_CIRCLE_CENTER, RADIUS, 180, 360, number_points)[:-1])


def infinity_sign(number_points: int) -> list[tuple[float,float]]:
    return (arc(UPPER_CIRCLE_CENTER, RADIUS, -90, 270, 2 * number_points)[:-1]
            + arc(LOWER_CIRCLE_CENTER, RADIUS, 90, -270, 2 * number_points)[:-1])


def scale_to_area(points: list[tuple[float,float]], area: tuple[float, float, float, float]) -> list[Point]:
    """were doing math in a simulation size like said in the assigment but then we  must convert it into actual pixels for the window logic"""
    x_min, y_min, x_max, y_max = area
    sx = (x_max - x_min) / SIMULATION_X
    sy = (y_max - y_min) / SIMULATION_Y
    
    return [Point(x_min + x * sx, y_min + y * sy) for x, y in points]