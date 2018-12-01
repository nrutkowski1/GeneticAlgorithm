from Initial.Dot import Dot
import random
import copy


class Population:

    # create a population of dots with a goal, surface to be drawn on, and a population size
    def __init__(self, size, goal, surface):

        self.goal = goal
        self.surface = surface
        self.size = size
        # sets the number of steps to be 1100 if a dot reaches the goal in fewer steps then this is updated
        self.minStep = 1100
        # the best dot will be set to be the first in the array of dots
        self.bestDot = 0
        # the generation number is update every iteration
        self.gen = 1
        self.fitnessSum = 0.0
        self.runningSum = 0.0
        # creates an array as the population of dots
        self.group = [None] * self.get_size()

        for i in range(0, self.get_size()):
            # add random dots to the population
            self.group[i] = Dot(self.get_goal(), self.get_surface())

    def get_goal(self): return self.goal

    def get_surface(self): return self.surface

    def get_min_step(self): return self.minStep

    def set_min_step(self, mi): self.minStep = mi

    def get_best(self): return self.bestDot

    def set_best(self, bs): self.bestDot = bs

    def get_gen(self): return self.gen

    def set_gen(self, g): self.gen = g

    def get_fitness_sum(self): return self.fitnessSum

    def set_fitness_sum(self, fs): self.fitnessSum = fs

    def get_group(self): return self.group

    def set_group(self, gr): self.group = gr

    def get_runningSum(self): return self.runningSum

    def set_runningSum(self, rs): self.runningSum = rs

    def get_size(self): return self.size

    # shows the dots on the surface
    def show_all(self):

        for i in range(1, len(self.get_group())):
                # show all of the dots in the population
                self.get_group()[i].show_dot(self.get_surface())
        # show the best dot
        self.get_group()[0].show_dot(self.get_surface())

    # update all of the dots in the population
    def update_all(self):

        for i in range(0, len(self.get_group())):
            # if the current step is greater than the minimum step the dot did not reach the goal in the required time
            if self.get_group()[i].get_brain().get_step() > self.get_min_step():
                # set it to be dead
                self.get_group()[i].set_dead(True)

            else:
                # otherwise update it
                self.get_group()[i].update()

    # calculate the fitness of all of the dots
    def calculate_fitness_all(self):

        for i in range(0, len(self.get_group())):

            self.get_group()[i].calculate_fitness()
            # print("fitness sum: " + str(self.group[i].calculate_fitness()))

    def all_dots_dead(self):
        # checks if all of the dots have died or reached the goal, if they have returned true
        for i in range(0, len(self.get_group())):

            if (not self.get_group()[i].get_dead()) and (not self.get_group()[i].get_reachedGoal()):

                return False

        return True

    # perform natural selection
    def natural_selection(self):

        # create a new group of dots
        newDots = self.get_group()
        # print("Old: " + str(self.group))
        # define the best dot from the group
        self.set_best_dot()
        # calculate the fitness sum
        self.calculate_fitness_sum()
        # set the first dot in the array to be the child of the best dot
        newDots[0] = self.get_group()[self.get_best()].reproduce()
        # define it as the best dot
        newDots[0].set_isBest(True)
        # print("alleged best fitness: " + str(self.get_group()[self.get_best()].get_fitness()))
        # print("new dots best: " + str(newDots[self.get_best()]))
        # print("og best: " + str(self.get_group()[self.get_best()]))

        # for the rest of the dots...
        for i in range(1, len(self.get_group())):
            # select a parent
            parent = self.select_parent()
            # print("parent: " + str(parent))
            # copy a child of the parent to a new group of dots
            newDots[i] = parent.reproduce()
        # create a copy of the new group of dots and set to the group of the population
        self.set_group(copy.copy(newDots))
        # print("New: " + str([self.group[1].pos.x, self.group[1].pos.y]))
        # print(str(newDots[0].get_isBest()) + " , " + str(newDots[1].get_isBest()))
        # increase and set the generation by one
        g = self.get_gen() + 1
        self.set_gen(g)
        # print("Gen: " + str(self.get_gen()))

    # calculate the fitness sum
    def calculate_fitness_sum(self):

        # set it to be 0
        self.set_fitness_sum(0.0)

        for i in range(0, len(self.get_group())):
            # add the fitness of all of the dots together
            fs = self.get_fitness_sum() + self.get_group()[i].get_fitness()
            self.set_fitness_sum(fs)

        # print(self.get_fitness_sum())

    # parent selection -- this should be worked on
    def select_parent(self):
        # get a random number between 0 and the fitness value
        rand = random.uniform(0, self.get_fitness_sum())
        # print(self.get_size())
        # get a running sum that is 0
        self.set_runningSum(0.0)

        for i in range(0, len(self.get_group())):

            # rewrite how select_parent and natural_selection work
            # set the running sum to be the current total of the sum of the fitness of each dot
            num = self.get_runningSum() + self.get_group()[i].get_fitness()
            self.set_runningSum(num)
            #print("Running Sum: " + str(self.get_runningSum()))
            #print("Rand: " + str(rand))
            #print("fitness: " + str(self.get_group()[i].get_fitness()))
            # if the running sum is larger then a random number
            if self.get_runningSum() > rand:

                # create a copy of the current dots and make a child of it
                d = self.get_group()[i]
                x = d.reproduce()
                x.get_brain()
                # x.get_brain().mutate10(0.007)

                return x

            # although a large majority of this is the best dot so idk about that
            r = random.randint(0, 5)
            # this does same as above but will be adjusted eventually....
            if r < 2:

                d = self.get_group()[self.get_best()]
                x = d.reproduce()
                # x.get_brain().mutate(0.06)
                x.get_brain()#.mutate10(0.01)

                return x

            else:

                d = self.get_group()[self.get_best()]
                x = d.reproduce()
                x.get_brain()#.mutate(0.005)
                #x.get_brain().mutate10(0.05)

                return x

        # this is a not so great option
        # return Dot(self.get_goal(), self.get_surface())

    # mutate the children
    def mutate_babies(self):

        for i in range(1, len(self.get_group())):
            # mutate all but the best dot form the previous generation at a rate of 0.01
            self.get_group()[i].get_brain().mutate(0.01)

    # set the best dot from the generation
    def set_best_dot(self):

        mx = 0.0
        maxIndex = 0

        # get the dot with the highest fitness
        for i in range(0, len(self.get_group())):

            if self.get_group()[i].get_fitness() > mx:

                mx = self.get_group()[i].get_fitness()
                maxIndex = i
        # set the ebst dot as the one with the highest fitness
        self.set_best(maxIndex)

        # print(self.get_group()[maxIndex])
        print("go farther")
        print("reached goal?: " + str(self.get_group()[self.get_best()].get_reachedGoal()))
        # if the best one reaches the goal
        if self.get_group()[self.get_best()].get_reachedGoal():
            # gets the steps of the dot that reached the goal and updates the minimum steps to that value
            ms = self.get_group()[self.get_best()].get_brain().get_step()
            self.set_min_step(ms)
            print("new: " + str(ms))
            print("step: " + str(self.get_min_step()))
            # print("step: %i" % self.get_min_step())

# Hypothesis: when the best dot doesnt change from generation to generation the fitness reverts back to 0?
