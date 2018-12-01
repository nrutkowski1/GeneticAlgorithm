
import pygame.math as pm
from random import uniform
import math


class Brain:

    # initialize a brain to have a step of 0, an empty array of directions of a specified size, and the randomize
    # the accleration vector in the array
    def __init__(self, size):

        s = 0

        self.directions = [None] * size
        self.randomize()
        self.step = s

    def get_directions(self): return self.directions

    def set_directions(self, direct, index): self.get_directions()[index] = direct

    def get_step(self): return self.step

    def set_step(self, step): self.step = step

    # this randomizes the vectors in the directions
    def randomize(self):
        # iterate over the array of directions
        for i in range(0, len(self.get_directions())):
            # get a random angle from 0 to 2pi or 0 to 360 degrees
            randomAngle = float(uniform(0, 2 * math.pi))
            # make a 2d vector from the random angle and set it equal to the acceleration vector
            self.get_directions()[i] = pm.Vector2(math.cos(randomAngle), math.sin(randomAngle))

    # clone the brain
    def clone(self):
        # makes a new brain of same length as the current
        clone = Brain(len(self.get_directions()))

        # print("og: " + str(self.get_directions()))
        # iterate over the list of directions
        for i in range(0, len(self.get_directions())):
            # copy the directions from the original brain to the new one
            clone.set_directions(self.get_directions()[i], i)

        # print("Clone: " + str(clone.get_directions()))
        # return the cloned brain
        return clone

    # mutates the entire length of directions at a constant rate
    def mutate(self, r):
        # sets the rate of mutation
        rate = r
        # iterate over the directions
        for i in range(0, len(self.get_directions())):
            # get a random number form 0 to 1
            rand = float(uniform(0, 1))
            # if the random number is less than the given rate
            if rand < rate:
                # generate a random angle, get a vector from it, and update the current directions vector to the new
                # random vector
                randomAngle = float(uniform(0, 2 * math.pi))
                x = pm.Vector2(math.cos(randomAngle), math.sin(randomAngle))
                self.set_directions(x, i)

    # mutates specifically the directions 5 before and preceding the final step
    def mutate10(self, r):
        # set the given rate of mutation
        rate = r
        # iterate from 5 steps before it died to the end of the array
        for i in range(self.get_directions().index(self.get_directions()[self.get_step()]) - 5,
                       len(self.get_directions())):

            rand = float(uniform(0, 1))

            if rand < rate:
                # set the direction to a new random one if a random number is less than the rate
                randomAngle = float(uniform(0, 2 * math.pi))
                x = pm.Vector2(math.cos(randomAngle), math.sin(randomAngle))
                self.set_directions(x, i)
