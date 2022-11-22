import random

import pygame as pg
import numpy as np

pg.init()
screen = pg.display.set_mode((800,600))

G = 0
'''Floor'''
F = 500
TIME = 0
t = 0.05

zippers = []
wells = []

class Zipper:
    def __init__(self, x, y, rotation, speed, size, c):
        self.x = x
        self.y = y
        self.s = size
        self.rot = rotation
        self.speed = speed
        self.color = c
        self.vel = [np.cos(rotation) * speed * t, np.sin(rotation) * speed * t]
        self.mass = 1
        zippers.append(self)

    def draw(self):
        xb, yb = self.x-np.cos(self.rot)*4,self.y-np.sin(self.rot)*4
        pg.draw.polygon(screen, self.color, ((self.x, self.y), (self.x + np.cos(self.rot+((3.6*np.pi)/4))*self.s, self.y+np.sin(self.rot+((3.6*np.pi)/4))*self.s), (self.x + np.cos(self.rot+((4.4*np.pi)/4))*self.s, self.y+np.sin(self.rot+((4.4*np.pi)/4))*self.s)))
        self.vel[1] += G*self.mass
        self.x += self.vel[0]
        self.y += self.vel[1]
        if self.vel[0] == 0:
            if self.vel[1] > 0:
                rot = np.pi/2
            if self.vel[1] < 0:
                rot = (3*np.pi)/2
        else:
            input = self.vel[1] / self.vel[0]
            self.rot = np.arctan(input)
        if self.y >= F and self.vel[1] > 0:
            self.vel[1] *= -0.6

    def force(self, x, y):
        self.x += x
        self.y += y

class Zipert:
    def __init__(self, x, y, rotation, timeforzips, zippermass):
        self.x = x
        self.y = y
        self.r = 4
        self.speed = 3
        self.rot = rotation
        self.time = timeforzips
        self.color = (255,255,0)
        self.zm = zippermass

    def draw(self):
        if np.abs(np.sin(TIME*(np.pi/(self.time*2)))) == 1:
            z = Zipper(self.x, self.y, self.rot, self.speed, 5, (0,255,0))
            z.mass = self.zm
        self.color = (np.abs(np.sin(TIME*(np.pi/(self.time*2))))*255, np.abs(np.sin(TIME*(np.pi/(self.time*2))))*255, 0)
        pg.draw.circle(screen, self.color, (self.x, self.y), self.r)

class Well:
    def __init__(self, x, y, gravity, killrad):
        self.x = x
        self.y = y
        self.G = gravity
        self.killrad = killrad
        self.r = self.killrad
        wells.append(self)

    def draw(self):
        pg.draw.circle(screen, (20,20,20), (self.x, self.y), self.r)
        for z in zippers:
            z.vel[0] += self.G*(self.x - z.x)*t
            z.vel[1] += self.G*(self.y - z.y)*t
            if np.sqrt((self.x - z.x)**2 + (self.y-z.y)**2) <= self.killrad:
                zippers.remove(z)


Z = Zipert(100,200,0,10,20)
W = Well(400,300,0.000001,20)

playing = True
while playing:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            for z in wells:
                z.G += 0.000001
        if keys[pg.K_s]:
            for z in wells:
                z.G -= 0.000001


    screen.fill((0, 5, 0))

    for z in zippers:
        z.draw()
    for w in wells:
        w.draw()

    Z.draw()
    TIME += t
    pg.display.update()