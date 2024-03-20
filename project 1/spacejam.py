from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
import DefensePaths as defensePaths
import SpaceJamClasses as spaceJamClasses
from CollideObjectBase import PlacedObject

class SpaceJam(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.SetupScene()
        
        self.cTrav = CollisionTraverser()                                                                                           #Goes through every collidable object in scene
        self.cTrav.traverse(self.render)                                                                                            #Traverse through everything in render node
        self.pusher = CollisionHandlerPusher()                                                                                      #Pusher for when 2 objects with colliders touch
        self.pusher.addCollider(self.Ship.collisionNode, self.Ship.modelNode)                                                       #Add collider to our 'from' object and pss it the geometry of our model
        self.cTrav.addCollider(self.Ship.collisionNode, self.pusher)                                                                #Allow that collider to be interacted with by others in scene
        self.cTrav.showCollisions(self.render)                                                                                      #See when collisions happen

        fullCycle = 60
        for j in range(fullCycle):
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.Planet4, nickName, j, fullCycle)
            
        defensePaths.CircleXY(self)
        defensePaths.CircleXZ(self)
        defensePaths.CircleYZ(self)
        self.SetCamera()
        

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/Drones/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/Drones/DroneDefender/octotoad1_auv.png", position, 10)

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/Drones/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/Drones/DroneDefender/octotoad1_auv.png", position, 5)

    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Ship.modelNode)
        self.camera.setFluidPos(0, 1, 0)

    def SetupScene(self):
            #Universe
        self.Universe = spaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render, 'Universe', "./Assets/Universe/starfield-in-blue.jpg", (0, 0, 0), 15000)

            #Spaceship
        self.Ship = spaceJamClasses.Spaceship(self.loader,"./Assets/Spaceships/Dumbledore/Dumbledore.egg", self.render, 'Ship', (0, 0, 0), 10, self.taskMgr, self.render, self.accept)

            #Planets
        self.Planet1 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/redPlanet.x", self.render, 'Planet1', "./Assets/Planets/Planet1.jpg", (150, 5000, 67), 350)
        self.Planet2 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/redPlanet.x", self.render, 'Planet2', "./Assets/Planets/Planet2.jpg", (5000, 1000, 183), 600)
        self.Planet3 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/redPlanet.x", self.render, 'Planet3', "./Assets/Planets/Planet3.png", (500, 9060, 23), 200)
        self.Planet4 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/redPlanet.x", self.render, 'Planet4', "./Assets/Planets/Planet4.png", (1000, 1833, 1000), 350)
        self.Planet5 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/redPlanet.x", self.render, 'Planet5', "./Assets/Planets/Planet5.png", (183, 500, 1500), 300)
        self.Planet6 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/redPlanet.x", self.render, 'Planet6', "./Assets/Planets/Planet6.png", (2000, 2000, 2300), 400)

            #Space Station
        self.Station = spaceJamClasses.SpaceStation(self.loader, "./Assets/SpaceStation/SpaceStation1B/spaceStation.egg", self.render, 'Station', (-1000, -1000, -1000), 40)
        
        


        

        
app = SpaceJam()
app.Ship.SetKeyBinding()
app.run()