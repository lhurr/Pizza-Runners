# CLASS: DAAA2B02
# Member 1: Yee Hang (2112675)
# Member 2: Lim Hur (2112589)
from queue import PriorityQueue
from cartesiangrid import CartesianGrid
from typing import Callable
from drone import Drone
import time
from turtle import Screen
from math import radians , sin,cos 
class PathFinder: 
    @staticmethod
    def leftHandRule(drone : Drone, startxindex : int, startyindex: int,screenupdate: Callable):
        """
        Left Hand Rule Algorithm
        Attributes: 
        :param drone: An instance of a drone. (turtle sprite)
        :param startxindex: Starting x coordinate position of drone 
        :param startyindex: Starting y coordinate position of drone 
        :param screenupdate: Callback function to update actions taken
        :return 
        """
        counter = 0   # Counter to keep track of actions taken (changing direction does not count as an action, actions are defined as moving forward)

        # This section is to check if there is a open path (NOT A WALL) on the left of the drone or not
        # If it is open, the drone would move forward until it touches a building and then proceed to turn right 
        # After this, the left hand rule can be used.
        # IF there is no open path, this section would be skipped and the left hand rule is applied
        initialleft :bool = drone.checkLeft()  # Check if there is an open path on left
        if initialleft: 
            drone.turnLeft() # If there is no building to the left of the drone, the drone turns left and moves forward until it reaches a building
            while drone.checkForward(): #Check if there is open path at the front of drone
                if drone.isAtDestination(): #Check if drone is at destination
                    return 1, counter 
                drone.moveForward() # Move the drone forward
                time.sleep(0.2)
                counter += 1 # Counter to keep track of number of forward moves taken.
                
            drone.turnRight() # Turn right so left hand rule can be used.
            startxindex =  drone.xpos # Update starting x coordinate
            startyindex = drone.ypos # Update starting y coordinate

        # The stop condition for left hand rule is the following: 
        first_ls =[] #Defines the first path taken by drone
        second_ls =[] # Defines the second path taken by drone

        list_pointer =first_ls # Keep a reference to the first path taken
        counterstopcond = 0 # Keeps track of how many times drone passes starting position
        firstpass = True # Denotes that this is the first pass of the LHR
        while True:
            if drone.isAtDestination():
                return 1, counter 
            if drone.xpos == startxindex and  drone.ypos == startyindex :
                if counterstopcond == 1:#after returning to start for first time , append the nodes passed by drone to node 2
                    list_pointer= second_ls
                elif counterstopcond > 1 : 
                    if first_ls == second_ls: # If the first list = second list, then we have no solution
                        return 0, None
                counterstopcond += 1 # Denotes that the drone has reached the starting point one time
                    
            # Implements the left hand rule algorithm. 
            firstpass = False # Denotes that it is no longer the first pass
            if drone.checkLeft():  #if there is no building on left
                drone.turnLeft()   # go left and move one step forward 
                drone.moveForward()
            elif drone.checkForward():   #if there is no building in front
                drone.moveForward()   #  move one step forward 
            elif drone.checkRight():   #if there is no building in right
                drone.turnRight()    #  go right and move one step forward 
                drone.moveForward()
            else:
                drone.turnRight()# If there is a building on left , front and right,  turn right twice (turn 180 degree) and move one step forward
                drone.turnRight()
                drone.moveForward() # Move forward

            # Append the path the drone took to our reference
            list_pointer.append((drone.xpos,drone.ypos))
            time.sleep(0.2)
            counter += 1 # Increment counter by 1 for every action taken
            screenupdate(f'{counter}') # Updates the screen for action taken

    @staticmethod  
    def heuristic(x1,x2 ,y1,y2):
        '''Heuristic for A*'''
        return (abs(x1 - x2) + abs(y1 - y2))
        # estimate from current point to destination 
        # heuristic is chosen as manhatten distance,  as it is the minimum distance to move from one point to another assuming no obstacles
        # manhatten distance is the same as the actual distance when there are no obstacles
    
    @staticmethod
    def aStar(map, startxindex, endxindex, startyindex, endyindex  ):
        """
        A star Algorithm
        Attributes: 
        :param map: the map (Cartesian Grid)
        :param startxindex: Starting x coordinate position of drone
        :param startyindex: Starting y coordinate position of drone
        :param endxindex:  Ending x coordinate position of drone
        :param endyindex: Ending y coordinate position of drone
        :param screenupdate: Callback function to update actions taken
        :return path, length of path 
        """
        height = len( map)
        width = len(map[0])
        fscores =CartesianGrid( [[float('inf')]*width for _ in range(height)])# create a grid with same shape as the maze to store f scores
        gscores =CartesianGrid( [[float('inf')]*width for _ in range(height)])# create a grid with same shape as the maze  to store g scores 
        visited =CartesianGrid( [[0]*width for _ in range(height)])#2d array of boolean in shape of map  to keep track of whether the element is inserted into the 

        opened = PriorityQueue() # use a priority queue to keep track of the nodes with highest f score and g score
        
        
        starth = PathFinder.heuristic( startxindex, endxindex, startyindex, endyindex ) #calculate f score from starting node to destination
        
        
        fscores[startxindex, startyindex] = starth # fscore of starting node
        gscores[startxindex, startyindex] = 0 # gscore is the distance from the starting node 
        visited[startxindex, startyindex ] = 1# to mark the inital node is visited 
        path = {} # to store the parent : child relationship of nodes {Node1 : Node2} means in the a star path the  path goes from 
        
        
        
        opened.put(((starth , starth) , ( startxindex, startyindex)))# insert the initial fscore and g score into the priority queue in  tuple as (fscore, heuristic)
                                                                     # both the  f score  and heuristic  is used in the priority queue
                                                                     # as it is possible for f score to be same between 2 different nodes 
                                                                    
                                                                     # hence , it requires the heuristic to be used as 'tie breaker' 
                                                                     
                                                                     
        
        while not opened.empty():#execute main loop as long as the priority queue is not empty 
            currnode = opened.get()[1]#get the node in the queue with lowest  f score, if f score is the same use heuristic as tie breaker
            currX , currY = currnode # get x and y coordinate 
            
            if currX == endxindex and currY == endyindex:  # check if reach the end
                finalpath = [currnode]# list to store the final path but in reverse order, we will loop thorugh the indexes in reverse in drone.
                #built the path using the parent child relationship recorded in path dictionary 
                while True:
                    currnode = path.get(currnode)# starting from from the end node ...
                    if currnode is not None: # ...while the path havent reach the start
                        finalpath.append(currnode) # add node to path...
                    else:
                        return finalpath, len(finalpath) #return the final path and the length of path found when reach the end of the path 
                
            
            for shiftx , shifty in [(0, -1), (0, 1), (-1, 0), (1, 0)]:# check neighbour of current node  in the North , South, East, West direction 
                #
                neighbourX = currX + shiftx #calculate x coordinate of neighbour
                neighbourY = currY  + shifty# calculate y coordinate of neighbour 
                
                try:
                    #skip the current neighbour if the current neighbour is outside map (indexing error) or the neighbour is building
                    if map[neighbourX, neighbourY] == 0:
                        continue 
                    
                except IndexError as e: # catching index error if the neighbour is outside the map, (means the current node is on the edge or corner of map )
                    continue 
                tempg = gscores[currX , currY] + 1 #calculate g score (distance from start to  neighbour node), passing through the current node
              
                if tempg < gscores[neighbourX, neighbourY]:# update g score if newer g score is lower 
                    path[(neighbourX, neighbourY) ] = (currX, currY )#set parent of neighbour node to current node, in the a* path the drone goes from current node to neighbour 
                    gscores[neighbourX, neighbourY] = tempg  #update gscore for neighbour
                    htemp = PathFinder.heuristic(endxindex, neighbourX, endyindex , neighbourY) #calculate manhatten distance from the neighbour node to the end position
                    ftemp =  tempg + htemp   # fscore = gscore + hscore
                    fscores[neighbourX, neighbourY] =ftemp # update the f score 
    
                    if not visited[neighbourX, neighbourY]: #if the node is not visited ....
                        visited[neighbourX, neighbourY] = 1 # mark the neighbour cell as visited
                        opened.put(((ftemp , htemp) , ( neighbourX, neighbourY)))#inserting both fscore and heuristic into the PriorityQueue, if the f score is the same, the priority queue takes the element with lower heuristic score

        return None , None  # the opened priority queue is empty and the destination node not reached there is no solution
    
    opposites = {'N':'S', 'S' :'N', 'E':'W', 'W' :'E'}
    directionalmapping = {'S':(0, -1),
                          'N':(0, 1),
                          'W':(1, 0),
                          'E':(-1, 0)
                          }

    
    @staticmethod  
    def heuristicwind(x1,x2 ,y1,y2 , windirection, windintensity,currentdirection):
        '''Heuristic for A*'''
        if len(windirection) ==1:
            if currentdirection == PathFinder.opposites[windirection]:#if moving against wind times 2 the g cost
                additionalterm=windintensity*0.1
                    
            elif currentdirection ==    windirection:#if moving same direction as wind divide by 2 the g cost
                additionalterm  = -(windintensity*0.1)
            else:
                additionalterm = 1
                
                
        else:
            sin45 = sin(radians(45))
            if  PathFinder.opposites[currentdirection] in windirection  :#wind blow opposite to drone
                
                
                additionalterm =  sin45*windintensity
                
            elif currentdirection in windirection:
                additionalterm =-sin45*windintensity
            else:
                additionalterm = 1
            
            
        if  windirection in {'N','S'}:
            additionalterm = additionalterm*abs(y1 - y2)
        else:
            additionalterm = additionalterm*abs(x1-x2)
                
    
        return (abs(x1 - x2) + abs(y1 - y2)) +additionalterm
        
        
        
    
    
    @staticmethod
    def calculate_g_score(moving_direction, wind_direction,windintensity,map, x,y,basegscore = 1):
        '''
        Extra feature by YH
        moving direction: N,S,E,W
        WIND direction: N,S,E,W,NE,NW,SE,SW,
        basegscore: original g score 
        This function alters the node weights based on the turbulance that could be encountered by drone
        
        '''
        newgscore = basegscore
        if len(wind_direction)==1:
            if moving_direction == PathFinder.opposites[wind_direction]:
                newgscore= basegscore+windintensity*0.1
                
            elif moving_direction ==    wind_direction:
                newgscore  = basegscore-(windintensity*0.1)
            else:
                newgscore = basegscore
                
        elif len(wind_direction)==2:
            sin45 = sin(radians(45))#calculate sin45 degree , 
            if  PathFinder.opposites[moving_direction] in wind_direction  :#wind blow opposite to drone
                
                
                newgscore = basegscore + sin45*windintensity
                
            elif moving_direction in wind_direction:
                newgscore = basegscore - sin45*windintensity
            else:
                newgscore = basegscore
        
        return newgscore
                
                
                
            
            
        
        
    @staticmethod
    def aStarWind(map, startxindex, endxindex, startyindex, endyindex , wind_direction  , windintensity):
        """
        Advance feature by YH
        A star Algorithm with wind 
        Attributes: 
        :param map: the map (Cartesian Grid)
        :param startxindex: Starting x coordinate position of drone
        :param startyindex: Starting y coordinate position of drone
        :param endxindex:  Ending x coordinate position of drone
        :param endyindex: Ending y coordinate position of drone
        :param screenupdate: Callback function to update actions taken
        :param windirection
        :return path, length of path 
        
        """
        height = len( map)
        width = len(map[0])
        fscores =CartesianGrid( [[float('inf')]*width for _ in range(height)])# create a grid with same shape as the maze to store f scores
        gscores =CartesianGrid( [[float('inf')]*width for _ in range(height)])# create a grid with same shape as the maze  to store g scores 
        visited =CartesianGrid( [[0]*width for _ in range(height)])#2d array of boolean in shape of map  to keep track of whether the element is inserted into the 

        opened = PriorityQueue() # use a priority queue to keep track of the nodes with highest f score and g score
        
        print(startxindex,startyindex)
        starth = PathFinder.heuristic( startxindex, endxindex, startyindex, endyindex ) #calculate f score from starting node to destination
        
        
        fscores[startxindex, startyindex] = starth # fscore of starting node
        gscores[startxindex, startyindex] = 0 # gscore is the distance from the starting node 
        visited[startxindex, startyindex ] = 1# to mark the inital node is visited 
        path = {} # to store the parent : child relationship of nodes {Node1 : Node2} means in the a star path the  path goes from 
        
        
        
        opened.put(((starth , starth) , ( startxindex, startyindex)))# insert the initial fscore and g score into the priority queue in  tuple as (fscore, heuristic)
                                                                     # both the  f score  and heuristic  is used in the priority queue
                                                                     # as it is possible for f score to be same between 2 different nodes 
                                                                    
                                                                     # hence , it requires the heuristic to be used as 'tie breaker' 
                                                                     
                                                                     
        
        while not opened.empty():#execute main loop as long as the priority queue is not empty 
            print(opened)
            currnode = opened.get()[1]#get the node in the queue with lowest  f score, if f score is the same use heuristic as tie breaker
            currX , currY = currnode # get x and y coordinate 
            visited[(currX,currY)] =0 
            
            if currX == endxindex and currY == endyindex:  # check if reach the end
                finalpath = [currnode]# list to store the final path but in reverse order, we will loop thorugh the indexes in reverse in drone.
                #built the path using the parent child relationship recorded in path dictionary 
                while True:
                    currnode = path.get(currnode)# starting from from the end node ...
                    if currnode is not None: # ...while the path havent reach the start
                        finalpath.append(currnode) # add node to path...
                    else:
                        return finalpath, len(finalpath) #return the final path and the length of path found when reach the end of the path 
                
            
            for directionstring, (shiftx , shifty) in PathFinder.directionalmapping.items():# check neighbour of current node  in the North , South, East, West direction 
                #
                neighbourX = currX + shiftx #calculate x coordinate of neighbour
                neighbourY = currY  + shifty# calculate y coordinate of neighbour 
                
                try:
                    #skip the current neighbour if the current neighbour is outside map (indexing error) or the neighbour is building
                    if map[neighbourX, neighbourY] == 0:
                        continue 
                    
                except IndexError as e: # catching index error if the neighbour is outside the map, (means the current node is on the edge or corner of map )
                    continue 
                tempg = gscores[currX , currY] + PathFinder.calculate_g_score(directionstring,wind_direction, windintensity ,map, neighbourX,neighbourY , 1 ) #calculate g score (distance from start to  neighbour node), passing through the current node
                print(tempg)
                if tempg < gscores[neighbourX, neighbourY]:# update g score if newer g score is lower 
                    path[(neighbourX, neighbourY) ] = (currX, currY )#set parent of neighbour node to current node, in the a* path the drone goes from current node to neighbour 
                    gscores[neighbourX, neighbourY] = tempg  #update gscore for neighbour
                    htemp = PathFinder.heuristicwind(endxindex, neighbourX, endyindex , neighbourY, wind_direction, windintensity, directionstring) #calculate manhatten distance from the neighbour node to the end position
                    ftemp =  tempg + htemp   # fscore = gscore + hscore
                    fscores[neighbourX, neighbourY] =ftemp # update the f score 
    
                    if not visited[neighbourX, neighbourY]: #if the node is not visited ....
                        visited[neighbourX, neighbourY] = 1 # mark the neighbour cell as visited
                        opened.put(((ftemp , htemp) , ( neighbourX, neighbourY)))#inserting both fscore and heuristic into the PriorityQueue, if the f score is the same, the priority queue takes the element with lower heuristic score

        return None , None  # the opened priority queue is empty and the destination node not reached there is no solution
    
    

