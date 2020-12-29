# In this file, we will define the Car class, with its constructor and methods.

import os
from math import *
from road import *
import numpy as np
import pygame as py
from random import random
from vect2d import vect2d
from config_variables import *

class Car:
    x = 0
    y = 0
    """
    Class variables: coordinates with respect to the global reference system, 
    the position on the screen is relative to the position of the best machine
    """

    def __init__(self, x, y, turn):
        self.x = x
        self.y = y
        self.rot = turn
        self.rot = 0
        self.vel = MAX_VEL/2
        self.acc = 0
        self.initImgs()
        self.commands = [0, 0, 0, 0]

    def initImgs(self):
        """
        Assign a random image for each car(agent) as well as account for deceleration
        (adding break lights image)
        """


        img_names = ["car1.png", "car2.png", "car3.png", "car4.png"]

        name = img_names[floor(random() * len(img_names)) % len(img_names)]


        self.img = py.transform.rotate(py.transform.scale(py.image.load(os.path.join("imgs", name)).convert_alpha(), (120, 69)), -90)
        self.brake_img = py.transform.rotate(py.transform.scale(py.image.load(os.path.join("imgs", "brakes.png")).convert_alpha(), (120, 69)), -90)

    def detectCollision(self, road):
        mask = py.mask.from_surface(self.img)   # ignores transparent parts of the images in order to detect if the intended image collides with other pixels
        (width, height) = mask.get_size()   # actual size of car body
        for v in [road.pointsLeft, road.pointsRight]:
            for p in v:
                x = p.x - self.x + width/2
                y = p.y - self.y + height/2
                try:
                    if mask.get_at((int(x), int(y))):
                        return True                 # if a car point touches a road point a collision is detected
                except IndexError as error:
                    continue
        return False

    def getInputs(self, world, road):           # win is used to draw the sensors if DBG = True
        sensors = []
        for k in range(8):
            sensors.append(SENSOR_DISTANCE)
        sensorsEquations = getSensorEquations(self, world)      # array of each segment equation

        for v in [road.pointsLeft, road.pointsRight]:
            i = road.bottomPointIndex
            while v[i].y > self.y - SENSOR_DISTANCE:
                next_index = getPoint(i+1, NUM_POINTS*road.num_ctrl_points)

                getDistance(world, self, sensors, sensorsEquations, v[i], v[next_index])
                i = next_index

        if CAR_DBG:
            for k,s in enumerate(sensors):
                omega = radians(self.rot + 45*k)
                dx = s * sin(omega)
                dy = - s * cos(omega)
                if s < SENSOR_DISTANCE:
                    py.draw.circle(world.win, RED, world.getScreenCoords(self.x+dx, self.y+dy), 6)

        for s in range(len(sensors)):
            sensors[s] = 1 - sensors[s]/SENSOR_DISTANCE

        return sensors

    def move(self, road, t):
        self.acc = FRICTION

        if decodeCommand(self.commands, ACC):
            self.acc = ACC_STRENGTH
        if decodeCommand(self.commands, BRAKE):
            self.acc = -BRAKE_STRENGTH
        if decodeCommand(self.commands, TURN_LEFT):
            self.rot -= TURN_VEL
        if decodeCommand(self.commands, TURN_RIGHT):
            self.rot += TURN_VEL

        timeBuffer = 500
        if MAX_VEL_REDUCTION == 1 or t >= timeBuffer:
            max_vel_local = MAX_VEL
        else:
            ratio = MAX_VEL_REDUCTION + (1 - MAX_VEL_REDUCTION) * (t / timeBuffer)
            max_vel_local = MAX_VEL * ratio

        self.vel += self.acc
        if self.vel > max_vel_local:
            self.vel = max_vel_local
        if self.vel < 0:
            self.vel = 0
        self.x = self.x + self.vel * sin(radians(self.rot))
        self.y = self.y - self.vel * cos(radians(self.rot))

        return (self.x, self.y)

    def draw(self, world):
        screen_position = world.getScreenCoords(self.x, self.y)
        rotated_img = py.transform.rotate(self.img, -self.rot)
        new_rect = rotated_img.get_rect(center=screen_position)
        world.win.blit(rotated_img, new_rect.topleft)

        if decodeCommand(self.commands, BRAKE):
            rotated_img = py.transform.rotate(self.brake_img, -self.rot)
            new_rect = rotated_img.get_rect(center=screen_position)
            world.win.blit(rotated_img, new_rect.topleft)

# ======================== HELPER FUNCTIONS ==========================

def getSensorEquations(self, world):
    """
    returns the equations of the straight lines (in variable y) of the
    machine in the following order:
    [vertical, increasing diagonal, horizontal, decreasing diagonal]
    """
    eq = []
    for i in range(4):
        omega = radians(self.rot + 45 * i)
        dx = SENSOR_DISTANCE * sin(omega)
        dy = - SENSOR_DISTANCE * cos(omega)

        if CAR_DBG:       # draw sensor lines
            py.draw.lines(world.win, GREEN, False, [world.getScreenCoords(self.x + dx, self.y + dy), world.getScreenCoords(self.x - dx, self.y - dy)], 2)

        coef = getSegmentEquation(self, vect2d(x=self.x + dx, y=self.y + dy))
        eq.append(coef)
    return eq

def getSegmentEquation(p, q):
    """
    equations in variable y between two points (taking into account the coordinate system
    with y inverted) in the general form ax + by + c = 0 (linear equation)
    """

    a = p.y - q.y
    b = q.x - p.x
    c = p.x * q.y - q.x * p.y

    return (a, b, c)

def getDistance(world, car, sensors, sensorsEquations, p, q):
    """
    for each given segment, calculate the distance and put it in the corresponding sensor
    """
    (a2, b2, c2) = getSegmentEquation(p, q)

    for i, (a1, b1, c1) in enumerate(sensorsEquations):         # get intersection between sensor and segment

        if a1 != a2 or b1 != b2:
            d = b1 * a2 - a1 * b2
            if d == 0:
                continue
            y = (a1 * c2 - c1 * a2) / d
            x = (c1 * b2 - b1 * c2) / d
            if (y - p.y) * (y - q.y) > 0 or (x - p.x) * (
                    x - q.x) > 0:           # if the intersection is not between a and b, go to the next iteration
                continue
        else:           # coincident lines
            (x, y) = (abs(p.x - q.x), abs(p.y - q.y))

        # get distance
        dist = ((car.x - x) ** 2 + (car.y - y) ** 2) ** 0.5

        # insert into the sensor in the right direction
        omega = car.rot + 45 * i            # angle of the sensor line (and its opposite)
        alpha = 90 - degrees(atan2(car.y - y, x - car.x))               # angle to vertical (as car.rot)
        if cos(alpha) * cos(omega) * 100 + sin(alpha) * sin(omega) * 100 > 0:
            index = i
        else:
            index = i + 4

        if dist < sensors[index]:
            sensors[index] = dist

def decodeCommand(commands, type):
    if commands[type] > ACTIVATION_THRESHOLD:
        if type == ACC and commands[type] > commands[BRAKE]:
            return True
        elif type == BRAKE and commands[type] > commands[ACC]:
            return True
        elif type == TURN_LEFT and commands[type] > commands[TURN_RIGHT]:
            return True
        elif type == TURN_RIGHT and commands[type] > commands[TURN_LEFT]:
            return True
    return False