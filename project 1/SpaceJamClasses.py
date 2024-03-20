from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *
from CollideObjectBase import *
from typing import Callable
from direct.gui.OnscreenImage import OnscreenImage

class Planet(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        #modelPath = geometry, parentNode = our render node, nodeName = name for node
        #texPath = bath in file to texture, posVec = where model shows, scaleVec = how model scaled
        super(Planet, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.02)                                    
                                                              
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Drone(SphereCollideObject):
    droneCount = 0                                                                              #how many drones have been spawned
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Drone, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.02)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9)
        
        
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Spaceship(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float, task, render, accept: Callable[[str, Callable], None]):
        self.accept = accept
        super(Spaceship, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.02)
        self.taskManager = task
        self.render = render
        self.loader = loader
        
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.reloadTime = .25
        self.missileDistance = 4000                                                                                             #until missile explodes
        self.missileBay = 1                                                                                                     #only 1 missle in missle bay to be launched
        
        self.EnableHUD()

        self.taskManager.add(self.CheckIntervals, 'checkMissiles', 34)

    def CheckIntervals(self, task):
        for i in Missile.Intervals:
            if not Missile.Intervals[i].isPlaying():                                                                                                #isPlaying returns true/false to see if missle gets to end of path
                Missile.cNodes[i].detachNode()                                                                                                      #if path done, get rid of everything to do with missile
                Missile.fireModels[i].detachNode()

                del Missile.Intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]

                print(i + ' has rached the end of its fire solution.')
                break
        return task.cont

    def Thrust(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskManager.remove('forward-thrust')

    def ApplyThrust(self, task):
        rate = 5
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()

        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont
    
    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyLeftTurn, 'left-turn')
        else:
            self.taskManager.remove('left-turn')

    def ApplyLeftTurn(self, task):
        rate = .5
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont
    
    def RightTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRightTurn, 'right-turn')
        else:
            self.taskManager.remove('right-turn')

    def ApplyRightTurn(self, task):
        rate = .5
        self.modelNode.setH(self.modelNode.getH() - rate)
        return Task.cont
    
    def UpTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyUpTurn, 'up-turn')
        else:
            self.taskManager.remove('up-turn')

    def ApplyUpTurn(self, task):
        rate = .5
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont
    
    def DownTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyDownTurn, 'down-turn')
        else:
            self.taskManager.remove('down-turn')

    def ApplyDownTurn(self, task):
        rate = .5
        self.modelNode.setP(self.modelNode.getP() - rate)
        return Task.cont
    
    def RotateLeft(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRotateLeft, 'left-rotate')
        else:
            self.taskManager.remove('left-rotate')

    def ApplyRotateLeft(self, task):
        rate = .5
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont
    
    def RotateRight(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRotateRight, 'right-rotate')
        else:
            self.taskManager.remove('right-rotate')

    def ApplyRotateRight(self, task):
        rate = .5
        self.modelNode.setR(self.modelNode.getR() - rate)
        return Task.cont
    
    def Fire(self):
        if self.missileBay:
            travRate = self.missileDistance
            aim = self.render.getRelativeVector(self.modelNode, Vec3.forward())                                                  #direction ship is facing
            aim.normalize()                                                                                                      #normalizing vector makes it consistant all the time
            fireSolution = aim * travRate
            inFront = aim * 150
            travVec = fireSolution + self.modelNode.getPos()
            self.missileBay -= 1
            tag = 'Missile' + str(Missile.missileCount)
            posVec = self.modelNode.getPos() + inFront                                                                           #spawn missile in front of nose of ship

            currentMissile = Missile(self.loader, './Assets/Spaceships/Phaser/phaser.egg', self.render, tag, posVec, 4.0)       #create missile

            Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)           #fluid = 1 = makes collision be checked between last interval and this interval
            Missile.Intervals[tag].start()
        else:
            if not self.taskManager.hasTaskNamed('reload'):                                                                         #if aren't reloading, start reloading
                print('Initializing reload...')

                self.taskManager.doMethodLater(0, self.Reload, 'reload')                                                            #call reload method on no delay
                return Task.cont
            
    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1
            if self.missileBay > 1:
                self.missileBay = 1
            print("Reload complete.")
            return Task.done
        elif task.time <= self.reloadTime:
            print("Reload proceeding...")
            return Task.cont
    
    def SetKeyBinding(self):
        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])
        self.accept('a', self.LeftTurn, [1])
        self.accept('a-up', self.LeftTurn, [0])
        self.accept('d', self.RightTurn, [1])
        self.accept('d-up', self.RightTurn, [0])
        self.accept('w', self.UpTurn, [1])
        self.accept('w-up', self.UpTurn, [0])
        self.accept('s', self.DownTurn, [1])
        self.accept('s-up', self.DownTurn, [0])
        self.accept('q', self.RotateLeft, [1])
        self.accept('q-up', self.RotateLeft, [0])
        self.accept('e', self.RotateRight, [1])
        self.accept('e-up', self.RotateRight, [0])
        self.accept('f', self.Fire)

    def EnableHUD(self):
        self.Hud = OnscreenImage(image = "./Assets/Spaceships/Hud/Reticle3b.png", pos = Vec3(0, 0, 0), scale = 0.1)
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)

class SpaceStation(CapsuleCollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

class Missile(SphereCollideObject):
    fireModels = {}
    cNodes = {}
    collisionSolids = {}
    Intervals = {}
    missileCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float = 1.0):
        super(Missile, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setPos(posVec)

        Missile.missileCount += 1

        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.collisionNode

        Missile.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
        Missile.cNodes[nodeName].show()
        
        print("Fire torpedo #" + str(Missile.missileCount))

    
    
