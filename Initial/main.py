import pygame as pg
from pygame import gfxdraw as fx
from Initial.Population import Population

# define the window size
width = 700
height = 700

# initialize the window and font
pg.display.init()
pg.font.init()

# create a background window set fill the surface color as white
background = pg.display.set_mode((width, height), 0, 8)
background.fill((255, 255, 255))

# define the goal at a specific coordinate
goal = fx.filled_circle(background, 320, 70, 5, (255, 0, 0))
goalpos = pg.math.Vector2(320, 70)

# create a population of 500 dots
test = Population(500, goalpos, background)

running = True

while running:

    # display in text the generation and minimum step to reach the goal
    genNum = pg.font.SysFont('Comic Sans MS', 20)
    textSurface = genNum.render("Generation: " + str(test.get_gen()) + "  MinStep: " + str(test.get_min_step()), False, (0, 0, 0))

    # if all of the dots are dead calculate the fitness, perform natural selection, mutate the new group
    if test.all_dots_dead():

        test.calculate_fitness_all()
        test.natural_selection()
        test.mutate_babies()
    # otherwise update all of the dots and show them
    else:

        test.update_all()
        test.show_all()
    # update both the display and text every 5 milliseconds
    background.blit(textSurface, (5, 5))
    pg.display.update()
    pg.time.delay(5)
    # this prevents trails from be created by resetting the background to filled white for a frame
    background.fill((255, 255, 255))
    goal = fx.filled_circle(background, 320, 70, 5, (255, 0, 0))

    # for closing the window
    for event in pg.event.get():

        if event.type == pg.QUIT:

            running = False

# mutation idea to implement:
# mutate along the range of steps that were taken by the dot before it died
# have the rate of mutation be gradual over this array of steps such that
# at the beginning little or even no mutations take place but as you approach
# the end of the directions array the frequency and in turn the number of mutations
# increases to allow for the dots to spread out and explore more closely to the best dot
# hopefully, this will lead to more of the dots being close to the best dot before they begin to spread out.

# build a random maze generator
# make use of graphs maybe matrix of cubes abc by 123
# walls of a thickness of 2 or so don't let the max velocity be larger than wall thickness
# otherwise will go through the walls
