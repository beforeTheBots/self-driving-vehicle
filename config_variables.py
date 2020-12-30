# In this file, we will define the variables what we will work with in each file, variables will include the following:

import pygame as py

py.font.init()  # initializes the font module. The module must be initialized before any other functions will work.

# 1. General Constants:
# =================== General constants ==================================
FPS = 30  # frame per second
WIN_WIDTH = 1500  # window width
WIN_HEIGHT = 800  # window height
STARTING_POS = (WIN_WIDTH / 2, WIN_HEIGHT - 100)
SCORE_VEL_MULTIPLIER = 0.00  # bonus for faster cars
BAD_GENOME_THRESHOLD = 200  # if a car is too far behind it is removed
INPUT_NEURONS = 9  # 8 neurons are distances to borders, 9 is the speed
OUTPUT_NEURONS = 4  # accelerate, brake, turn left, turn right

# 2. Car Specifications:
# =========================== Car Specs ==================================
CAR_DBG = False
FRICTION = -0.1  # the allowed friction rate
MAX_VEL = 10  # maximum speed
MAX_VEL_REDUCTION = 1  # at the start, reduce speed to 1
ACC_STRENGTH = 0.2  # acceleration strength
BRAKE_STRENGTH = 1  # brake strength
TURN_VEL = 2  # the speed of turning
SENSOR_DISTANCE = 200  # the distance of sensor from borders
ACTIVATION_THRESHOLD = 0.5  #

# 3. Road Specifications:
# ========================== Road Specs ==================================
ROAD_DBG = False
MAX_ANGLE = 1  # maximum accepted road angle
MAX_DEVIATION = 300  # maximum accepted road deviation
SPACING = 200  # the higher the easier
NUM_POINTS = 15  # number of points for each segment
SAFE_SPACE = SPACING + 50  # buffer space above the screen
ROAD_WIDTH = 215  # width of the road, the higher the easier

# 4. Display and Colors:
# =================== Display and Colors =================================
NODE_RADIUS = 20
NODE_SPACING = 5
LAYER_SPACING = 40
CONNECTION_WIDTH = 1

WHITE = (255, 255, 255)
GRAY = (193,154,107)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
DARK_RED = (100, 0, 0)
RED_PALE = (250, 200, 200)
DARK_RED_PALE = (150, 100, 100)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
GREEN_PALE = (200, 250, 200)
DARK_GREEN_PALE = (100, 150, 100)
YELLOW = (255,255,1)


NODE_FONT = py.font.Font("fonts/Debrosee-ALPnL.ttf", 15)
STAT_FONT = py.font.Font("fonts/PixelEmulator-xq08.ttf", 30)

# 5. Constants for internal use:
# =================== Constants for internal use =========================
GEN = 0  # generation

# enumerations (in output layer)
ACC = 0  # acceleration index
BRAKE = 1  # brake index
TURN_LEFT = 2  # turn left index
TURN_RIGHT = 3  # turn right index

# neural network layers
INPUT = 0
MIDDLE = 1
OUTPUT = 2
