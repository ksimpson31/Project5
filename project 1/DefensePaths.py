import math, random
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

def Cloud(radius = 1):
    x = 2 * random.random() - 1
    y = 2 * random.random() - 1
    z = 2 * random.random() - 1

    unitVex = Vec3(x, y, z)
    unitVex.normalize()
    return unitVex * radius

def BaseballSeams(step, numSeams, B, F = 11):
    time = step / float(numSeams) * 2 * math.pi

    F4 = 0

    R = 1

    xxx = math.cos(time) - B * math.cos(3 * time)
    yyy = math.sin(time) + B * math.sin(3 * time)
    zzz = F * math.cos(2 * time) + F4 * math.cos(4 * time)

    rrr = math.sqrt(xxx ** 2 + yyy ** 2 + zzz ** 2)

    x = R * xxx / rrr
    y = R * yyy / rrr
    z = R * zzz / rrr

    return Vec3(x, y, z)

def CircleXY(self):
    self.drone = self.loader.loadModel("./Assets/Drones/DroneDefender/DroneDefender.obj")

    x = 0
    for i in range(60):
        theta = x
        self.placeholder2 = self.render.attachNewNode('Placeholder2')
        self.placeholder2.setPos(50.0 * math.cos(theta), 50.0 * math.sin(theta), 0.0)
        self.placeholder2.setColorScale(1.0, 0.0, 0.0, 1.0)
        self.drone.instanceTo(self.placeholder2)
        x = x + 0.11

def CircleXZ(self):
    self.drone = self.loader.loadModel("./Assets/Drones/DroneDefender/DroneDefender.obj")

    x = 0
    for i in range(60):
        theta = x
        self.placeholder2 = self.render.attachNewNode('Placeholder2')
        self.placeholder2.setPos(50.0 * math.cos(theta), 0.0, 50.0 * math.sin(theta))
        self.placeholder2.setColorScale(0.0, 1.0, 0.0, 1.0)
        self.drone.instanceTo(self.placeholder2)
        x = x + 0.11

def CircleYZ(self):
    self.drone = self.loader.loadModel("./Assets/Drones/DroneDefender/DroneDefender.obj")

    x = 0
    for i in range(60):
        theta = x
        self.placeholder2 = self.render.attachNewNode('Placeholder2')
        self.placeholder2.setPos(0.0, 50.0 * math.sin(theta), 50.0 * math.cos(theta))
        self.placeholder2.setColorScale(0.0, 0.0, 1.0, 1.0)
        self.drone.instanceTo(self.placeholder2)
        x = x + 0.11