##make a game where we introduce the new class as a stationary object, we will add button to draw points on the screen 
#then connect those points into a new phisical object, and apply phisics to that object, the point is that the user will have 
#to draw a shape that helps them hit the targets. kinda like brain lines

#todo list:
#-implement phisical body 
#-make a way so that the ball interacts with the phisical body and windows etc
#-build example maps, make maping of best score to map
#-build the file to hold different pre loaded maps
#-build thing so that user can choose and save maps
import json
import math
from graphics import GraphWin, GraphicsError, Line, Point, Text, update
from config.loader import load_scenario
from config.types_config import Scenario
from graphical_logic.classes import Ball, Button, Character, Target
#