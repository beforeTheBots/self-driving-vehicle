# In this file, we will draw the Neural Network that will be displayed on the screen of the app.
import pygame as py
from config_variables import *
from car import decodeCommand
from vect2d import vect2d
from node import *
py.font.init()
class NN:
    def __init__(self, config, genome, pos):
        self.input_nodes = []
        self.output_nodes = []
        self.nodes = []
        self.genome = genome
        self.pos = (int(pos[0]+NODE_RADIUS), int(pos[1]))
        input_names = ["Sensor T", "Sensor TR", "Sensor R", "Sensor BR", "Sensor B", "Sensor BL", "Sensor L", "Sensor TL", "Speed"]
        output_names = ["Accelerate", "Brake", "Turn Left", "Turn Right"]
        middle_nodes = [n for n in genome.nodes.keys()]
        nodeIdList = []
        #nodes
        h = (INPUT_NEURONS-1)*(NODE_RADIUS*2 + NODE_SPACING) # the height of inputs column which have and it is 360
        for i, input in enumerate(config.genome_config.input_keys):
            n = Node(input, pos[0], pos[1]+int(-h/2 + i*(NODE_RADIUS*2 + NODE_SPACING)), INPUT, [GREEN_PALE, GREEN, DARK_GREEN_PALE, DARK_GREEN], input_names[i], i)
            # n have the parameter of input nodes like it's position on x and y, it's type (INPUT type = 0), colors, it's lable (like Sensor T) and the node index
            self.nodes.append(n)
            nodeIdList.append(input)
        h = (OUTPUT_NEURONS-1)*(NODE_RADIUS*2 + NODE_SPACING) # the height of output column which have and it is 135
        for i,out in enumerate(config.genome_config.output_keys):
            n = Node(out+INPUT_NEURONS, pos[0] + 2*(LAYER_SPACING+2*NODE_RADIUS), pos[1]+int(-h/2 + i*(NODE_RADIUS*2 + NODE_SPACING)), OUTPUT, [RED_PALE, RED, DARK_RED_PALE, DARK_RED], output_names[i], i)
            # n have the parameter of output nodes like it's position on x and y, it's type (INPUT type = 2), colors, it's lable (like Accelerate) and the node index
            self.nodes.append(n)
            middle_nodes.remove(out)
            nodeIdList.append(out)