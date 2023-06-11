# CLASS: DAAA2B02
# Member 1: Yee Hang (2112675)
# Member 2: Lim Hur (2112589)

import turtle
from typing import Tuple, List
from time import sleep

# Defines a drone, which is a turtle.Turtle (sprite)
class Drone(turtle.Turtle):
    # Defines a mapping dictionary to map the resulting clockwise direction from any of the 4 directions
    CLOCKWISE= {
        'N' : 'E' , 
        'E' : 'S' , 
        'S' : 'W' , 
        'W' : 'N'
    }
    # Defines a mapping dictionary to map the resulting anticlockwise direction from any of the 4 directions
    ANTICLOCKWISE= {
        'N' : 'W' , 
        'W' : 'S' ,
        'S' :'E' , 
        'E' : 'N'
    }
    def __init__(self, startposx, startposy,  posxindex , posyindex,desxindex,desyindex, map, step_size ):
        super().__init__()
        self.__posxindex = posxindex # Keeps track of the current x coordinate of the drone
        self.__posyindex = posyindex # Keeps track of the current x coordinate of the drone
        self.__desxindex = desxindex # Defines the destination x coordinate
        self.__desyindex = desyindex # Defines the destination y coordinate
        self.__startposx = startposx # Defines the start x coordinate
        self.__startposy = startposy # Defines the start y coordinate
        self.__map = map  #Defines our map, which is also the cartesian grid; The drone has a map so that it "knows where it is on the map"


        # Defines the configuration of the drone.
        self.speed('slow')  # Set turtle speed to slow for visibility
        self.left(90)  # turtle spawns facing east as a default so make a 90 degree left turn for it to face north 
        self.orient = 'N' 
        self.step_size = step_size 
        self.color('black')  
        self.penup()  
        self.goto( (self.__startposx  + posxindex*self.step_size + self.step_size/2 , self.__startposy + posyindex*self.step_size + self.step_size/2))
        self.pendown()
        
        
        # Defines which direction to look at given the current drone's direction.
        self.__directionLookup = {
            'N': {'Forward' : self.__absoluteUp, 'Right' : self.__absoluteRight, 'Left':self.__absoluteLeft},
            'S': {'Forward' : self.__absoluteDown, 'Right' :self.__absoluteLeft, 'Left':self.__absoluteRight},
            'E' : {'Forward' :self.__absoluteRight , 'Right' :self.__absoluteDown, 'Left':self.__absoluteUp},
            "W": {'Forward' : self.__absoluteLeft, 'Right' :self.__absoluteUp, 'Left':self.__absoluteDown}
        }
    
    #Encapsulation: only getters defined for __posxindex and __posyindex making them read only   
    @property
    def xpos(self):
        return self.__posxindex 
    
    @property
    def ypos(self):
        return self.__posyindex

    # Moves the drone one position to the left -> imagine x axis shift back by one
    def __absoluteLeft(self) -> Tuple[int, int]:
        return self.__posxindex-1,self.__posyindex # Returns the new position x and y index
    
    # Moves the drone one position to the right -> imagine x axis shift to the right
    def __absoluteRight(self) -> Tuple[int, int]:
        return self.__posxindex+1,self.__posyindex
      
    # Moves the drone to up -> shifting the drone upwards in the y axis
    def __absoluteUp(self) -> Tuple[int, int]:
        return self.__posxindex,self.__posyindex+1
    
    # Moves the drone downwards -> shift the drone in the y axis downwards
    def __absoluteDown(self) -> Tuple[int, int]:
        return self.__posxindex,self.__posyindex-1
        
    # Turns the drone to the right, changing its orientation
    def turnRight(self):
        self.orient = self.CLOCKWISE[self.orient]
        self.right(90)
    # Turns the drone to the left, changing its orientation
    def turnLeft(self):
        self.orient = self.ANTICLOCKWISE[self.orient]
        self.left(90)
 
    
    # Move forward one step by a step size, based on the orientation the drone is in.
    # Updates the position x, and position y index.
    def moveForward(self):
        self.forward(self.step_size)
        self.__posxindex , self.__posyindex = self.__directionLookup[self.orient]['Forward']()

    # ====================================== VERIFICATION METHODS =============================================

    # Get the directional coordinates based on the relative location of the drone
    def getRelativeDirec(self,direction):
        return self.__directionLookup[self.orient][direction]()

    # Check if the path on the right is not a building
    def checkRight(self) -> bool:
        x, y = self.__directionLookup[self.orient]['Right']() # Get the x, and y index of where the drone would be if it took a right turn
        try:
            return self.__map[x,y ] != 0# or self.isAtDestination(x,y)
        except IndexError:
            return False 
        
    # Check if the path on the left is not a building
    def checkLeft(self) -> bool:
        x,y = self.__directionLookup[self.orient]['Left']()
        try:
            return self.__map[x,y ] != 0
        except IndexError:
            return False

    # Check if the path forward is not a building
    def checkForward(self):
        x,y = self.__directionLookup[self.orient]['Forward']()

        try:
            return self.__map[x,y ] != 0 
        except IndexError:
            return False 
    
    # Check if drone is at the destination
    def isAtDestination(self , x= None,y=None) -> bool:
        return self.__posxindex == self.__desxindex and self.__posyindex == self.__desyindex # Check if x and y coordinates with current position match with end x,y coorindates

    # Method for drone to follow the path, in the form of list of tuples generated by algorithm
    def followpath(self, path : List[Tuple[int,int]], screenupdater, reverse = False):
        """
        Lets the drone follow the path
        Params: 
        :param path: List[Tuple[int,int]]: Path in the form of list of tuples for the drone to move 
        :param screenUpdater: Callback function to update number of actions taken by algorithm
        :param reverse: Whether to path provided is reversed or not. In tha case of A*, it is reversed.
        :return -
        """
        counter = 0   # Defines the counter for number of actions taken
        indexes = range(len(path) -1 , -1 ,  -1) if reverse else range(len(path))   # Defines the sequence of the path
        increment = -1 if reverse else 1 

        # Loop through the length of the path
        for idx,i in enumerate(indexes):
            coordinates = path[i] # Get the coordinates in tuple form
            
            x,y = coordinates #Get the x y coordinates for every step of the path
            self.penup() if idx == 0 else self.pendown() # Pen Up if drone moves to the start location

            # Let drone go to the specified coordinates found by algorithm.
            self.goto( (self.__startposx  + x*self.step_size + self.step_size/2 , self.__startposy + y*self.step_size + self.step_size/2))

            if idx !=0: # Since we do not count going to starting point as one action, we do not increment the counter.
                counter +=1 # Increment the counter for action steps only

            # Update the action counter at every step
            screenupdater(f'{counter}')

            # Set the direction of our drone is facing
            try:
                nextx, nexty = path[i+increment]# calculate the next coordinates
                diffx = nextx - x # calculate the change in x coordinate
                diffy = nexty - y # calculate change in y in coordinate
                
                
                # the codes below is to let the arrow face the direction the drone is going to travel in the next iteration 
                
                if diffx ==0 :# if change in x in 0 ,means there is a change in y coordinates
                    if diffy > 0 :
                        # if change in y is positive , so arrow face north as drone moves north in next iteration 
                        self.orient = 'N'
                        self.setheading(90)
                    else:
                        #else, change in y negative , so   arrow face south as drone moves south in next iteration 
                        self.orient = 'S'
                        self.setheading(270)
                        
                else:# else change in y is 0 , which means there is a change in x coordinates
                    if diffx > 0 :
                        # change in x coordinate negative means moving in east direction, so the drone face east
                        self.orient = 'E'
                        self.setheading(0)
                        
                    else:
                        # change in x coordinate positive means moving in west direction, so the drone face west
                        
                        self.orient = 'W'
                        self.setheading(180)

            except IndexError:
                pass
            sleep(0.15) # Slows down the drone