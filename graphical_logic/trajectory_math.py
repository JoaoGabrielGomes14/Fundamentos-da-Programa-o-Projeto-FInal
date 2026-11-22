import math
from graphics import Point
#assigment asks for for it to run in a simulated size, here is 1,2  . we then convert it to the pixel size for graphical logic
#line and arc are helpers to build the other shapes.

SIMULATION_X = 1.0
SIMULATION_Y = 2.0

RADIUS = 0.5

LOWER_CIRCLE_CENTER = (0.5,0.5)
UPPER_CIRCLE_CENTER = (0.5,1.5)

HEART_LOBE_RADIUS = 0.25
HEART_LEFT_LOBE_CENTER = (0.25,1.5)
HEART_RIGHT_LOBE_CENTER = (0.75,1.5)
HEART_TIP = (0.5,0.25)


def line(start:tuple[float,float],end:tuple[float,float],number_points:int)->list[tuple[float,float]]:
    """take start and endpoint, density and make a list of points"""
    points: list[tuple[float,float]] = []
    (x1,y1) , (x2,y2) = start,end

    for point in range(number_points+1):
        points.append(
            (x1 + (x2 - x1) * point / number_points, y1 + (y2 - y1) * point / number_points)
        )
    return points


def arc(center: tuple[float, float], radius: float,start_deg: float, end_deg: float, n: int) -> list[tuple[float,float]]:
    """take the start and end points and anfles aand give back an arc"""
    cx, cy = center
    points: list[tuple [float,float]] = []

    for i in range(n + 1):
        angle = math.radians(start_deg + (end_deg - start_deg) * i / n)
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return points


def ring(number_points:int) -> list[tuple[float,float]]:
    """make ring shape"""
    return (line((1, 0.5), (1, 1.5), number_points)[:-1]
            + arc(UPPER_CIRCLE_CENTER, RADIUS, 0, 180, number_points)[:-1]
            + line((0, 1.5), (0, 0.5), number_points)[:-1]
            + arc(LOWER_CIRCLE_CENTER, RADIUS, 180, 360, number_points)[:-1])


def infinity_sign(number_points: int) -> list[tuple[float,float]]:
    """build the infinity /oito shape"""
    return (arc(UPPER_CIRCLE_CENTER, RADIUS, -90, 270, 2 * number_points)[:-1]
            + arc(LOWER_CIRCLE_CENTER, RADIUS, 90, -270, 2 * number_points)[:-1])


def heart(number_points: int) -> list[tuple[float,float]]:
    """give the heart shape(our shape)"""
    return (line(HEART_TIP, (1, 1.5), number_points)[:-1]
            + arc(HEART_RIGHT_LOBE_CENTER, HEART_LOBE_RADIUS, 0, 180, number_points)[:-1]
            + arc(HEART_LEFT_LOBE_CENTER, HEART_LOBE_RADIUS, 0, 180, number_points)[:-1]
            + line((0, 1.5), HEART_TIP, number_points)[:-1])


def normalize(points: list[tuple[float,float]]) -> list[tuple[float,float]]:
    """convert from the scake in the csv and turn it into simulation size"""
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    if width == 0 and height == 0:
        raise ValueError("all the points in the file are the same point")

    scale = min(SIMULATION_X / width if width else math.inf,
                SIMULATION_Y / height if height else math.inf)
    x_offset = (SIMULATION_X - width * scale) / 2
    y_offset = (SIMULATION_Y - height * scale) / 2
    return [((x - min(xs)) * scale + x_offset, (y - min(ys)) * scale + y_offset) for x, y in points]


def read_trajectory_csv(path: str) -> list[tuple[float,float]]:
    points: list[tuple[float,float]] = []
    with open(path) as f:
        for line_number, row in enumerate(f, start=1):
            row = row.strip()
            if not row:
                continue
            values = row.split(",")
            if len(values) != 2:
                raise ValueError(f"line {line_number} should be 'x,y'")
            try:
                points.append((float(values[0]), float(values[1])))
            except ValueError:
                raise ValueError(f"line {line_number} is not two numbers")
    if len(points) < 2:
        raise ValueError("the file needs at least 2 points")
    return points


def scale_to_area(points: list[tuple[float,float]], area: tuple[float, float, float, float]) -> list[Point]:
    """convert from simulation to pixels on screen"""
    x_min, y_min, x_max, y_max = area
    sx = (x_max - x_min) / SIMULATION_X
    sy = (y_max - y_min) / SIMULATION_Y
    
    return [Point(x_min + x * sx, y_min + y * sy) for x, y in points]