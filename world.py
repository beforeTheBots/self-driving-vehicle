# In this file, we will define the scoring of the neurons.
import pygame as py

class World:
    # class attributes
    initialPos = (0, 0)
    bestCarPos = (0, 0)

    def __init__(self, starting_pos, world_width, world_height):

        self.initialPos = starting_pos
        self.bestCarPos = (0, 0)
        self.win = py.display.set_mode((world_width, world_height))
        self.win_width = world_width
        self.win_height = world_height
        self.score = 0  # Starting from 0 and increasing.
        self.bestGenome = None

    def updateBestCarPos(self, pos):  # update the best position oh the best car.
        self.bestCarPos = pos

    def getScreenCoords(self, x, y):  # calculate the distance of the best car .
        return (int(x + self.initialPos[0] - self.bestCarPos[0]), int(y + self.initialPos[1] - self.bestCarPos[1]))

    def getBestCarPos(self):  # return the position of the best car.
        return self.bestCarPos

    def updateScore(self, new_score):  # update the score.
        self.score = new_score

    def getScore(self):
        return self.score
