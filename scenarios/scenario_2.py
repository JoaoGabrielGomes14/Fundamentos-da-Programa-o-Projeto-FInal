from tkinter.filedialog import askopenfilename
from graphics import GraphWin, GraphicsError, Line, Point, Rectangle, Text,update
from config.loader import load_scenario
from graphical_logic.classes import Button, Target
from graphical_logic.trajectory_math import ring, infinity_sign, heart, normalize, read_trajectory_csv, scale_to_area

TRAJECTORIES = {
    "ring": ring,
    "eight": infinity_sign,
    "free": heart,
}


def draw_path(window: GraphWin, points: list[Point], color: str) -> list[Line]:
    """draws the path on the screen"""
    segments: list[Line] = []
    for i in range(0, len(points), 2):
        segment = Line(points[i], points[(i + 1) % len(points)])
        segment.setOutline(color)
        segment.draw(window)
        segments.append(segment)
    return segments


def load_trajectory_file(area: tuple[float, float, float, float]) -> list[Point] | None:
    
    path = askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*")])
    if not path:
        return None
    return scale_to_area(normalize(read_trajectory_csv(path)), area)


def run_scenario_2() -> None:
    scenario = load_scenario("scenario2")
    window = scenario.window.make_window()
    area = scenario.trajectory_area
    
    if area is None or scenario.targets is None:
        raise ValueError("scenario2 needs trajectory_area and targets in the config")
    
    x_min, y_min, x_max, y_max = area
    Rectangle(Point(x_min, y_min), Point(x_max, y_max)).draw(window)  #draw box where the pathes go

    buttons: dict[str, Button] = {}

    for button_settings in scenario.buttons:
        buttons[button_settings.id] = Button(window, button_settings) 
    message = Text(Point(*scenario.hud["message_position"]), "")
    message.setTextColor(scenario.hud["message_color"])
    message.draw(window)

    number_points: int = scenario.physics["number_points"]
    fps: int = scenario.physics["fps"]
    path_lines: list[Line] = []
    selected: str | None = None
    flyer: Target | None = None
    window.update()

    while True:
        try:
            click = window.checkMouse()
        except GraphicsError:
            return

        if buttons["quit"].clicked(click):
            break

        new_points: list[Point] | None = None
        clicked_id: str | None = None

        for trajectory_id, make_trajectory in TRAJECTORIES.items():
            if buttons[trajectory_id].clicked(click):
                new_points = scale_to_area(make_trajectory(number_points), area)  
                clicked_id = trajectory_id

        if buttons["load"].clicked(click):
            try:
                new_points = load_trajectory_file(area)
                clicked_id = "load"
            except (OSError, ValueError) as error:
                message.setText(f"Could not load the file: {error}")

        if new_points is not None and clicked_id is not None:
            message.setText("")
            if selected is not None:
                buttons[selected].deselect()
            buttons[clicked_id].select()
            selected = clicked_id

            for segment in path_lines:
                segment.undraw()
            path_lines = draw_path(window, new_points, scenario.hud["path_color"])

            if flyer is None:
                flyer = Target(window, scenario.targets, new_points)
            else:
                flyer.set_path(new_points)

        if flyer is not None:
            flyer.step()
        try:
            update(fps)
        except GraphicsError:
            return

    window.close()