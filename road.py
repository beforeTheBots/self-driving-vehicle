# In this file, we will define the Road class, with its constructor and methods.

from config_variables import *
import pygame as py
import numpy as np
from scipy import interpolate
from math import *
from vect2d import *
from random import random, seed

class Road:
    def __init__(self, world):  # world -> input
        self.num_ctrl_points = (int)((world.win_height + SAFE_SPACE) / SPACING) + 2

        self.last_ctrl_point = 0
        self.ctrl_points = []
        self.centerPoints = []
        self.pointsLeft = []
        self.pointsRight = []

