import os
import sys

import neat
import time

import random
import pygame as py


from car import *
from NNdraw import NN
from road import *
from world import World
from pygame.locals import *
from moviepy.editor import *
from config_variables import *
from  vect2d import *
from node import *


def test_car_create():
    car = Car(150, 100, 0)
    assert car.x == 150
    assert car.y == 100
    assert car.rot == 0
    print("PASSED - Car Creation")

def test_vect2d_create():
    vect = vect2d()
    assert vect.x != None
    assert vect.y != None
    print("PASSED - Vector Creation")

def test_world_create():
    world = World(STARTING_POS, WIN_WIDTH, WIN_HEIGHT)
    assert world.initialPos == STARTING_POS
    assert world.win_width == WIN_WIDTH
    assert world.win_height == WIN_HEIGHT
    print("PASSED - World Creation")

def test_road_create():
    world = World(STARTING_POS, WIN_WIDTH, WIN_HEIGHT)
    road = Road(world)
    assert road.bottomPointIndex == 0
    print("PASSED - Road Creation")

def test_node_create():
    node = Node(2, 5, 10, INPUT, [])
    assert node.id == 2
    assert node.x == 5
    assert node.y == 10
    assert node.type == INPUT
    assert node.color == []
    print("PASSED - Node Creation")


def test_collision_true():
    world = World(STARTING_POS, WIN_WIDTH, WIN_HEIGHT)
    road = Road(world)
    count_left = 1
    count_right = 1
    for pl in road.pointsLeft:
        pl.co(1, count_left)
        count_left += 1
    for pr in road.pointsRight:
        pl.co(300, count_right)
        count_right += 1
    car = Car(1, 2, 0)
    assert car.detectCollision(road) == True
    print("PASSED - Collision")

def test_collision_false():
    world = World(STARTING_POS, WIN_WIDTH, WIN_HEIGHT)
    road = Road(world)
    count_left = 1
    count_right = 1
    for pl in road.pointsLeft:
        pl.co(1, count_left)
        count_left += 1
    for pr in road.pointsRight:
        pl.co(300, count_right)
        count_right += 1
    car = Car(150, 2, 0)
    assert car.detectCollision(road) == False
    print("PASSED - No Collision")

def test_move():
    world = World(STARTING_POS, WIN_WIDTH, WIN_HEIGHT)
    road = Road(world)
    count_left = 1
    count_right = 1
    for pl in road.pointsLeft:
        pl.co(1, count_left)
        count_left += 1
    for pr in road.pointsRight:
        pl.co(300, count_right)
        count_right += 1
    car = Car(150, 100, 0)
    x = car.move(road, 0)[0]
    y = int(car.move(road, 0)[1])
    assert  x == 150
    assert y == 90
    print("PASSED - Movement Positions")

def test_commands_brake():
    assert decodeCommand([0.5, 0.6, 0.1, 0.0], 1) == True
    print("PASSED - Brake")

def test_commands_acc():
    assert decodeCommand([0.9, 0.7, 0.1, 0.0], 0) == True
    print("PASSED - Acceleration")

def test_commands_left():
    assert decodeCommand([0.5, 0.6, 0.6, 0.0], 2) == True
    print("PASSED - Turn Left")

def test_commands_right():
    assert decodeCommand([0.5, 0.6, 0.6, 0.8], 3) == True
    print("PASSED - Turn Right")

def test_get_point():
    assert getPoint(5,10) == 5
    print("PASSED - Point Retrieval")

def test_vect2d_get():
    vect = vect2d(5, 10)
    assert vect.getCo()[0] == 5
    assert vect.getCo()[1] == 10
    print("PASSED - Getting from Vector")

def test_vect2d_set():
    vect = vect2d()
    vect.co(5, 10)
    assert vect.x == 5
    assert vect.y == 10
    print("PASSED - Setting Vector Values")





if __name__ == "__main__":
    test_collision_true()
    test_collision_false()
    test_move()
    test_commands_brake()
    test_commands_acc()
    test_commands_left()
    test_commands_right()
    test_get_point()
    test_vect2d_create()
    test_vect2d_get()
    test_vect2d_set()
    test_car_create()
    test_world_create()
    test_road_create()
    test_node_create()
