import math



Points : list[tuple[float,float]] = []

SIMULATION_X = 1.0
SIMULATION_Y = 2.0

RADIUS = 0.5

LOWER_CIRCLE_CENTER = (0.5,0.5)
UPPER_CIRCLE_CENTER = (0.5,1.5)

def line(start:tuple[float,float],end:tuple[float,float],number_points:int)->list[tuple[float,float]]:
    line = []
    (x1,y1) , (x2,y2) = start,end

    for point in range(number_points+1):
        line.append(
            (x1 + (x2 - x1) * point / number_points, y1 + (y2 - y1) * point / number_points)
        )
    return line


def arc()