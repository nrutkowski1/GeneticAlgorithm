import pygame.math as pm
from pygame import gfxdraw as fx
from Initial.Brain import Brain
from Initial.Barrier import Barrier


class Dot(Brain, Barrier):

    def __init__(self, goal, surface):

        # the brain of the object, this gives directions, mutates, randomness
        self.brain = Brain(1100)
        # the surface it is drawn on - pygame object
        self.surface = surface
        # initial starting x,y position and velocities
        x_pos = 320
        y_pos = 600
        x_vel = 0.0
        y_vel = 0.0
        # set position and velocity as 2d vectors
        self.pos = pm.Vector2(x_pos, y_pos)
        self.vel = pm.Vector2(x_vel, y_vel)
        # initialize acceleration vector
        self.accl = pm.Vector2(0, 0)
        # initialize if its dead, reached the goal, or best dot
        self.dead = False
        self.reachedGoal = False
        self.isBest = False
        # set the goal - 2d vector to get to
        self.goal = goal
        # initialize fitness to be 0 - hasn't traveled yet
        self.fitness = 0.0

# best way is to have getters and setters for each object attribute
    def get_brain(self): return self.brain

    def set_brain(self, b): self.brain = b

    def get_xpos(self): return self.pos.x

    def set_xpos(self, x): self.pos.x = x

    def get_ypos(self): return self.pos.y

    def set_ypos(self, y): self.pos.y = y

    def get_xvel(self): return self.vel.x

    def set_xvel(self, xvel): self.vel.x = xvel

    def get_yvel(self): return self.vel.y

    def set_yvel(self, yvel): self.vel.y = yvel

    def get_accl(self): return self.accl

    def set_accl(self, a): self.accl = a

    def get_dead(self): return self.dead

    def set_dead(self, d): self.dead = d

    def get_reachedGoal(self): return self.reachedGoal

    def set_reachedGoal(self, rg): self.reachedGoal = rg

    def get_isBest(self): return self.isBest

    def set_isBest(self, ib): self.isBest = ib

    def get_fitness(self): return self.fitness

    def set_fitness(self, f): self.fitness = f

    def get_goal(self): return self.goal

    def get_pos(self): return self.pos

    def get_surface(self): return self.surface

    def show_dot(self, surface):

        # draw the objects - best one is green
        if self.get_isBest():

            fx.filled_circle(surface, int(self.get_xpos()), int(self.get_ypos()), 5, (0, 255, 0))

        else:

            fx.filled_circle(surface, int(self.get_xpos()), int(self.get_ypos()), 3, (0, 0, 0))

    # moves the dots with some generated randomness
    def move(self):
        # iterate over the directions while it is greater than the min step
        if len(self.get_brain().get_directions()) > self.get_brain().get_step():
            # acceleration vectors is the random vector at that step
            a = self.get_brain().get_directions()[self.get_brain().get_step()]
            # set it
            self.set_accl(a)
            # increase step
            num = self.get_brain().get_step() + 1
            # print("step: " + str(num))
            # set the step
            self.get_brain().set_step(num)

        else:
            # if it reaches end of directions array kill it
            self.set_dead(True)

        # mess around with these to change the movement
        # added self.get_accl() here makes it different for sure and lowered the max velocity magnitude
        if (((self.get_xvel() + self.get_accl().x) ** 2) + ((self.get_yvel() + self.get_accl().y) ** 2)) < 64.0:
            # add acceleration to velocity
            xl = self.get_xvel() + self.get_accl().x
            yl = self.get_yvel() + self.get_accl().y
            # update velocity
            self.set_xvel(xl)
            self.set_yvel(yl)
            # add velocity to position
            xp = self.get_xpos() + self.get_xvel()
            yp = self.get_ypos() + self.get_yvel()
            # update position
            self.set_xpos(xp)
            self.set_ypos(yp)
            # SET THE POSITION HERE
            # print("less than 5")

        else:
            # self.set_xvel(0.1*(self.get_xvel() + self.get_accl().x))
            # self.set_yvel(0.1*(self.get_yvel() + self.get_accl().y))
            # below not bad may be better than above
            # reset the velocity to an acceleration vector if velocity gets to large
            self.set_xvel(self.get_accl().x)
            self.set_yvel(self.get_accl().y)
            # add velocity to position
            xp = self.get_xpos() + self.get_xvel()
            yp = self.get_ypos() + self.get_yvel()
            # xv = self.get_xvel() - self.get_accl().x
            # yv = self.get_yvel() - self.get_accl().y
            # update position
            self.set_xpos(xp)
            self.set_ypos(yp)
            # self.set_xvel(xv)
            # self.set_yvel(yv)

        # print([self.get_xpos(), self.get_ypos()])

    def update(self):
        # define a box to be a barrier will update this for a random maze generator
        box1 = Barrier(self.get_surface(), 0, 400, 325, 300)
        box2 = Barrier(self.get_surface(), 300, 700, 200, 175)
        box3 = Barrier(self.get_surface(), 200, 700, 450, 425)
        # if the position is close to the goal
        if self.get_pos().distance_to(self.get_goal()) < 5.0:

            # set reachedGoal to be true
            self.set_reachedGoal(True)
        # if the dot has not made it to the goal and it has not died yet
        if not self.get_reachedGoal() and not self.get_dead():
            # move the dot
            self.move()
            # if the position is near the border of the screen
            if self.get_xpos() < 2 or self.get_ypos() < 2 or self.get_xpos() > 638 or self.get_ypos() > 638:
                # set it to be dead
                self.set_dead(True)
            # if it make it to the goal
            if self.get_pos().distance_to(self.get_goal()) < 5.0:

                # set reached goal to be true
                self.set_reachedGoal(True)
            # if it hits one of the three boxes then set it to be dead
            if (box1.get_leftp() < self.get_xpos() < box1.get_rightp() and
                    (box1.get_botp() < self.get_ypos() < box1.get_topp())):

                self.set_dead(True)

            if (box2.get_leftp() < self.get_xpos() < box2.get_rightp() and
                    (box2.get_botp() < self.get_ypos() < box2.get_topp())):

                self.set_dead(True)

            if (box3.get_leftp() < self.get_xpos() < box3.get_rightp() and
                    (box3.get_botp() < self.get_ypos() < box3.get_topp())):

                self.set_dead(True)

    # this will calculate the fitness of the dots. The fitness depends on how close the dot is to the goal
    # or if it reaches the goal the number of steps it took to reach the goal better dots will have a higher fitness
    # i.e. they are closer to the goal
    def calculate_fitness(self):
        # if it reaches the goal
        if self.get_reachedGoal():
            # the fitness is based on the steps it took to reach the goal
            f = (1.0/16.0) + 10000.0/(self.get_brain().get_step() * self.get_brain().get_step())
            self.set_fitness(f)

        else:
            # if it does not reach the goal its fitness is based on the distance to the goal
            distanceToGoal = self.get_pos().distance_to(self.get_goal())
            f = 0.1 + (1.0 / (distanceToGoal * distanceToGoal))
            self.set_fitness(f)

    # reproduce makes a new dot that is a replica of the parent it is copying
    def reproduce(self):

        child = Dot(self.get_goal(), self.get_surface())
        newBrain = self.get_brain().clone()
        child.set_brain(newBrain)
        return child
