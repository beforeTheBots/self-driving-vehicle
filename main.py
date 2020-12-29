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
import sys
from pygame.locals import *

py.init()
py.mixer.pre_init(44100, 16, 2, 4096)
py.font.init()
mainClock = py.time.Clock()
bg = py.Surface((WIN_WIDTH, WIN_HEIGHT))
bg.fill(GRAY)

py.display.set_caption('Race against Time!')
screen = py.display.set_mode((WIN_WIDTH, WIN_HEIGHT), 0, 32)
# crash = py.mixer.Sound('tracks/Glass and Metal Collision.mp3')

font = py.font.SysFont(None, 50)
logo = py.font.SysFont(None, 80)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    click = False

    py.mixer.music.stop()
    music = py.mixer.music.load('tracks/AlanWalker.mp3')
    py.mixer.music.play(-1)


    while True:

        screen.fill((255,255,255))
        draw_text('BEFORE THE BOTS!', logo, (0, 0, 0), screen, WIN_WIDTH-WIN_WIDTH*0.68, WIN_HEIGHT-WIN_HEIGHT*0.70)


        mx, my = py.mouse.get_pos()

        # BUTTON ONE :
        draw_text('PLAY GAME!', font, (0, 0, 0), screen, WIN_WIDTH-WIN_WIDTH*0.77, WIN_HEIGHT-WIN_HEIGHT*0.25)
        button_1 = py.Rect(WIN_WIDTH-WIN_WIDTH*0.8, WIN_HEIGHT-WIN_HEIGHT*0.2, 300, 50)

        # BUTTON TOW :
        draw_text('BOT PLAYER!', font, (0, 0, 0), screen, WIN_WIDTH-WIN_WIDTH*0.38, WIN_HEIGHT-WIN_HEIGHT*0.25)
        button_2 = py.Rect(WIN_WIDTH-WIN_WIDTH*0.4, WIN_HEIGHT-WIN_HEIGHT*0.2, 300, 50)
        if button_1.collidepoint((mx, my)):

            if click:
                round = 0
                single_play(round)
        if button_2.collidepoint((mx, my)):
            if click:
                local_dir = os.path.dirname(__file__)
                config_path = os.path.join(local_dir, "config_file.txt")
                run(config_path)
        py.draw.rect(screen, (0, 0, 255), button_1)
        py.draw.rect(screen, (0, 0, 255), button_2)

        click = False
        for event in py.event.get():
            if event.type == QUIT:
                py.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    py.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        py.display.update()
        mainClock.tick(60)

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
    for event in py.event.get():
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                main_menu()
    mainClock.tick(60)





def draw_single(cars, road, world, round):

    road.draw(world)
    for car in cars:
        car.draw(world)

    text = STAT_FONT.render("Score: " + str(int(world.getScore())), 1, BLACK)
    world.win.blit(text, (world.win_width - text.get_width() - 10, 10))
    text = STAT_FONT.render("Round: " + str(round), 1, BLACK)
    world.win.blit(text, (world.win_width - text.get_width() - 10, 50))



    py.display.update()
    world.win.blit(bg, (0,0))


def single_play(round):
    py.mixer.music.stop()
    music = py.mixer.music.load('tracks/Ratatouille\'s Kitchen - Carmen María and Edu Espinal.mp3')


    py.mixer.music.play(-1)

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
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    py.mixer.music.stop()
                    main_menu()
            mainClock.tick(60)

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
                1] + BAD_GENOME_THRESHOLD or y > y_old or car.vel < 0.1):  # il t serve a evitare di eliminare macchine nei primi tot frame (nei primi frame getCollision() restituisce sempre true)
                py.mixer.music.stop()
                py.mixer.Sound.play((crash))
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
        NNs.append(NN(config, g, (120, 250)))

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

            if t>10 and (car.detectCollision(road) or y > world.getBestCarPos()[1] + BAD_GENOME_THRESHOLD or y>y_old or car.vel < 0.1):
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

    py.mixer.music.stop()
    music = py.mixer.music.load('tracks/LinkinPark .mp3')
    py.mixer.music.play(-1)

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats =neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 10000)



if __name__ == "__main__":

    # local_dir = os.path.dirname(__file__)
    # config_path = os.path.join(local_dir, "config_file.txt")
    # run(config_path)
    # round = 0
    # single_play(round)
    main_menu()
