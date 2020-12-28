# In this file, we will run the training model using defined classes

import pygame as py
import neat
import time
import os
import random
from car import Car
from road import Road
from world import World
from NNdraw import NN
from config_variables import *
import time
py.font.init()


bg = py.Surface((WIN_WIDTH, WIN_HEIGHT))
bg.fill(GRAY)


def draw_win(cars, road, world, GEN):
    road.draw(world)
    for car in cars:
        car.draw(world)

    text = STAT_FONT.render("Best Car Score: "+str(int(world.getScore())), 1, BLACK)
    world.win.blit(text, (world.win_width-text.get_width() - 10, 10))
    text = STAT_FONT.render("Gen: "+str(GEN), 1, BLACK)
    world.win.blit(text, (world.win_width-text.get_width() - 10, 50))

    world.bestNN.draw(world)

    py.display.update()
    world.win.blit(bg, (0,0))

def draw_single(cars, road, world, round):

    road.draw(world)
    for car in cars:
        car.draw(world)

    text = STAT_FONT.render("Best Car Score: " + str(int(world.getScore())), 1, BLACK)
    world.win.blit(text, (world.win_width - text.get_width() - 10, 10))
    text = STAT_FONT.render("Round: " + str(round), 1, BLACK)
    world.win.blit(text, (world.win_width - text.get_width() - 10, 50))



    py.display.update()
    world.win.blit(bg, (0,0))


def single_play(round):
    round+=1
    start = time.perf_counter()

    cars = []
    t = 0

    world = World(STARTING_POS, WIN_WIDTH, WIN_HEIGHT)
    world.win.blit(bg, (0, 0))
    '''win is in world file which have the method for display our screen after that we use blit method which allowed 
    to draw two draws on each other the first parameter is the source of the displayed screen and the tuple is the 
    (dest) parameter which specify the coordinate for the next screen '''





    cars.append(Car(0, 0, 0))  # creating a car object


    road = Road(world)
    clock = py.time.Clock()

    run = True
    while run:
        t += 1
        clock.tick(FPS)
        world.updateScore(0)

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()

        (xb, yb) = (0, 0)
        i = 0
        while (i < len(cars)):
            car = cars[i]

            input = car.getInputs(world, road)
            input.append(car.vel / MAX_VEL)
            left, right, breakk = 0,0,0
            if event.type == py.KEYDOWN:

                if event.key == py.K_LEFT:
                    left = 1
                if event.key == py.K_RIGHT:
                    right = 1

            car.commands = [1, breakk, left, right]
            y_old = car.y
            (x, y) = car.move(road, t)

            if t > 10 and (car.detectCollision(road) or y > world.getBestCarPos()[
                1] + BAD_GENOME_TRESHOLD or y > y_old or car.vel < 0.1):  # il t serve a evitare di eliminare macchine nei primi tot frame (nei primi frame getCollision() restituisce sempre true)

                time.sleep(1)

                single_play(round)


            else:
                end = time.perf_counter() - start
                if (start > world.getScore()):
                    world.updateScore(end)
                i += 1

            if y < yb:
                (xb, yb) = (x, y)



        world.updateBestCarPos((xb, yb))
        road.update(world)
        draw_single(cars, road, world, round)



def main(genomes = [], config = []):
    global GEN
    GEN += 1

    nets = []
    ge = []
    cars = []
    t = 0

    world = World(STARTING_POS, WIN_WIDTH, WIN_HEIGHT)
    world.win.blit(bg, (0,0))

    NNs = []

    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(Car(0, 0, 0))
        g.fitness = 0
        ge.append(g)
        NNs.append(NN(config, g, (90, 210)))

    road = Road(world)
    clock = py.time.Clock()

    run = True
    while run:
        t += 1
        clock.tick(FPS)
        world.updateScore(0)

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
                quit()

        (xb, yb) = (0,0)
        i = 0
        while(i < len(cars)):
            car = cars[i]

            input = car.getInputs(world, road)
            input.append(car.vel/MAX_VEL)
            car.commands = nets[i].activate(tuple(input))

            y_old = car.y
            (x, y) = car.move(road,t)

            if t>10 and (car.detectCollision(road) or y > world.getBestCarPos()[1] + BAD_GENOME_TRESHOLD or y>y_old or car.vel < 0.1):
                ge[i].fitness -= 1
                cars.pop(i)
                nets.pop(i)
                ge.pop(i)
                NNs.pop(i)
            else:
                ge[i].fitness += -(y - y_old)/100 + car.vel*SCORE_VEL_MULTIPLIER
                if(ge[i].fitness > world.getScore()):
                    world.updateScore(ge[i].fitness)
                    world.bestNN = NNs[i]
                    world.bestInputs = input
                    world.bestCommands = car.commands
                i += 1

            if y < yb:
                (xb, yb) = (x, y)


        if len(cars) == 0:
            run = False
            break

        world.updateBestCarPos((xb, yb))
        road.update(world)
        draw_win(cars, road, world, GEN)


#NEAT function
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats =neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 10000)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_file.txt")
    run(config_path)
    # round = 0
    # single_play(round)
