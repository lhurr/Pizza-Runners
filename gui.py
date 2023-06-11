# CLASS: DAAA2B02
# Member 1: Yee Hang (2112675)
# Member 2: Lim Hur (2112589)
from generator import MazeGenerator 
from util import Util
import turtle, random
from drone import Drone
from pathfinder import PathFinder
from cartesiangrid import CartesianGrid
from TurtleGrid import TurtleGrid
from multipathfinder import MultiplePathFinder
from bitmask import BitMask

class GUI:
    '''
    Graphical User Interface class support what the user experiences
    '''
    def __init__(self):
        self.__currentAlgo = 'LeftHand'
        self.__map = None #initialise the map to none 
        self.__drone = None # initialise the drone to none 
        self.__mapDrawer = None
                                                                    # note THAT 'D' IS FOR EXTRA FEATURE
        self.__symbolToNumber = { 'X' : 0,'.' : 1 , 's':3 , 'e' : 4, 'D': 5} # X: wall, '.' represents open path; s represents START point; 'e' represent end point, this will be replaced by the path
        self.__squareDIM = 20 # make the length and width of each square 20 pixels at the start
        

    def run(self):
   
        self.__screen = turtle.Screen()

        # Event listeners to listen for key inputs from users. 
        # Supports press of 'n': for loading of map, 
        # 'Tab': Switching of algorithms, 
        # 'f': Use the current selected algorithm to find a path,
        # 'q': For quitting of program
        self.__loadMap()#ask user for a map 
        self.__eventHandlerOn()# turn on the event handler
        self.__screen.onkeypress(lambda : self.__screen.bye() ,'q')# allow user press q to quit the application 
        self.__screen.title(f'{self.__currentAlgo}')# specify current algo in screen
        
        self.__screen.listen()# listen for events
        self.__screen.mainloop() # enter the turtle main loop 
        
        
    def __switchAlgo(self, custom_algo=False):
        if custom_algo:
            self.__currentAlgo = custom_algo
            self.__screen.title(custom_algo)
            return
         
        #detect tab press and switch algo
        if self.__currentAlgo == 'LeftHand':
            self.__currentAlgo = 'A*'
        else:
            self.__currentAlgo = 'LeftHand'
        self.__screen.title(f'{self.__currentAlgo}')
        
    def __askHeight_width(self, prompt):
        while True:
            value = turtle.textinput('Generate Maze' ,prompt)# ask user for value
            self.__screen.listen() 
            if value is  None:
                return
            value = value.strip()
            if not value.isnumeric():
                prompt = 'the input contains non numbers\nPlease Enter only numbers\nPlease ensure input only has integers'
                continue
            
            if int(value) <= 8:
                prompt = 'value must be larger than 8'
                continue
            
            
            return value 

    def __generate_map( self):
        
        height = self.__askHeight_width('Please enter height of generated maze')
        if height is None:
            return 
        width = self.__askHeight_width('Please enter width of generated maze')
        if  width is None :
            return 
        
  
            

        generator = MazeGenerator(height=int(height),width=int(width))
        print(generator.verticalmappings['N'])

        self.__map = generator.create_maze()   
        self.__preparemap() 
        
    def __preparemap(self):
    
        width = len(self.__map[0])
        height = len(self.__map)
    
        
        totalwidth = width*self.__squareDIM
        totalheight = height *self.__squareDIM
        self.startposy = -totalheight/2 # ensure whole map is centralised of screen
        self.startposx  = -totalwidth / 2  
        textpos  = self.startposx + totalwidth /2, self.startposy + totalheight # calculate position of text, in the middle of the top screen 

        # Clear existing map to place the new map
        if self.__mapDrawer is not None :
            self.__mapDrawer.clear() # clear the map 
            self.__mapDrawer.ht() # hide the turtle to to prevent it overlapping with the new map  

        
        self.__mapDrawer = TurtleGrid() # instanciate a turtle grid 
        self.__mapDrawer.speed('fastest')
        self.__screen.tracer(0, 0)# turn of screen update per step , to prevent seeing each cell being updated
        self.startxindex , self.startyindex , self.endxindex ,self.endyindex = self.__mapDrawer.draw_maze(self.__map , self.__squareDIM, self.startposx, self.startposy )
        self.__mapDrawer.goto(textpos)# move the pen to the position where the text is placed 
        self.__mapDrawer.write('MAZE RUNNERS', align = 'center')# write the project 
        self.__screen.update()# update the screen

        self.__screen.tracer(1, 20) # turn the turtle screen auto update back on 
    
    

    def __loadMap(self):
        prompt_msg = 'Enter the filepath to the map \nPlease kindly ensure the map file format is appropriate'
        while True:
            path = turtle.textinput('Loading File' ,prompt_msg)# ask user for file
            self.__screen.listen() 
            if not path:
                self.__screen.bye()#if user input nothing close the scren
                return 
            contents , status = Util.read_file(path) # read the file in as string
            if status == 1:# status = 1 means the input in invalid , and reprompt the user 
                prompt_msg = contents
                continue 
            contents = contents.replace(' ' , '')#remove all spaces in file 
            lines = contents.splitlines()#split lines
            lines = [ innerarr.strip() for innerarr in lines if len(innerarr) != 0 ]# remove trailing and precedding spaces
            try:
                arr = list(map( lambda  line : [ self.__symbolToNumber[char] for char in line] ,lines))#  replace each character with numbers
            except Exception as e:
                # the above code will throw exception if the file format is wrong
                print(e)
                prompt_msg = 'File format is invalid! Please retry'
                continue

            if Util.check_jagged_array(arr):# check if array is jagged ( the array length and width is different)
                prompt_msg ='Array is not aligned properly'
                continue 
            self.mapLoaded = True
            self.__map =CartesianGrid(arr)  #instanciate the cartesion grid
            self.__preparemap()# prepare the map to be printed on screen 
            break        
        
    def __eventHandlerOff(self):
        #disable event listener 
        self.__screen.onkeypress(None, 'n')
        self.__screen.onkeypress(None, 'f')
        self.__screen.onkeypress(None, 'Tab')
        self.__screen.onkeypress(None, '1')
        self.__screen.onkeypress(None, '2')
        self.__screen.onkeypress(None ,'3')
        self.__screen.onkeypress(None, '4')
        
            

    def __eventHandlerOn(self):
        #enable the  event listener
        self.__screen.onkeypress(lambda : self.__loadMap(), 'n')
        self.__screen.onkeypress(lambda : self.__switchAlgo() , 'Tab')
        self.__screen.onkeypress(lambda : self.__findPath() , 'f')
        self.__screen.onkeypress(lambda : self.__allShortestPath(), '1')
        self.__screen.onkeypress(lambda : self.__findShortestWithDropOff(), '2')
        self.__screen.onkeypress(lambda : self.__findAstarPathWind() ,'3')
        self.__screen.onkeypress(lambda : self.__generate_map() ,'4')
        
    def __askwindintensity(self):
        prompt = 'Please key in the wind intensity from 2 to 110'
        while True:
            value = turtle.textinput('Wind Pathfinding' ,prompt)# ask user for value
            self.__screen.listen() 
            if value is  None:
                return
            value = value.strip()
            if not value.isnumeric():
                prompt = 'the input contains non numbers\nPlease Enter only numbers\nPlease ensure input only has integers'
                continue            
            if int(value) <= 1 or  int(value)  > 111:
                prompt = 'value must be larger than 1 and smaller than 110'
                continue
            return value 
        
    def __askwinddirection(self):
        prompt = "Please key in the wind  direction\none of 'N' ,'S' , 'E' , 'W' , 'NE' ,'NW', 'SE' , 'SW'"
        while True:
            value = turtle.textinput('Wind Pathfinding' ,prompt)# ask user for value
            self.__screen.listen() 
            if value is  None:
                return
            value = value.strip().upper() 
                 
            if value not in ['N' ,'S' , 'E' , 'W' , 'NE' ,'NW', 'SE' , 'SW']:
                prompt = "value must be one of 'N' ,'S' , 'E' , 'W' , 'NE' ,'NW', 'SE' , 'SW'"
                continue
            return value 
   
    def __findAstarPathWind(self):
        if self.__map is None:
            return
        if self.__drone is not None:
            self.__drone.clear() # clear drawing of previous algo 
            self.__drone.ht() 

        self.__eventHandlerOff()# dont allow user to change algo , import new file and restart pathfinding, by disabling event listener
        windintensity =self.__askwindintensity() #random.choice( [10,30,50,70,90,110])
        
        if windintensity is None:
            return 
        direction = self.__askwinddirection() #random.choice(['N' ,'S' , 'E' , 'W' , 'NE' ,'NW', 'SE' , 'SW'])
        if direction is None:
            return 
        windintensity = int(windintensity)
        path , length= PathFinder.aStarWind(self.__map, self.startxindex, self.endxindex, self.startyindex, self.endyindex  , direction , windintensity)# find the a star path  , if no valid path, return none as path 
        # the 
        print(path)
        if path is None:
            self.__screen.title(f'{self.__currentAlgo} No Path Found')#imform user in title screen if no path found 
            
        else:
            #instanciate the drone to walk the path 
            self.__drone  = Drone(self.startposx , self.startposy, self.startxindex  , self.startyindex , self.endxindex, self.endyindex,  self.__map , self.__squareDIM)
            # follow the path found by the path finder
            self.__drone.followpath(path, lambda step :self.__screen.title(f'Actions taken by Astar with wind blowing from {direction} direction: {step}, wind intensity {windintensity}'), reverse= True)
        self.__screen.title(f'Actions taken by Astar with wind blowing from {direction} direction: {length}, wind intensity {windintensity}')
        self.__eventHandlerOn()
        # self.__switchAlgo()
        
        
    def __findPath(self):
        if self.__map is None:
            return
        if self.__drone is not None:
            self.__drone.clear() # clear drawing of previous algo 
            self.__drone.ht() 

        self.__eventHandlerOff()# dont allow user to change algo , import new file and restart pathfinding, by disabling event listener

        if self.__currentAlgo == 'LeftHand':
            # instanciate the drone
            self.__drone = Drone( self.startposx , self.startposy, self.startxindex  , self.startyindex , self.endxindex, self.endyindex,  self.__map , self.__squareDIM)
            # the path finder uses the drone to walk on the map, and returns whether there is a valid path from start to end for left hand
            status, length   = PathFinder.leftHandRule(self.__drone, self.startxindex, self.startyindex , self.update_screen) 

            if status:
                self.__screen.title(f'{self.__currentAlgo} in {length} step')
            else:
                self.__screen.title(f'{self.__currentAlgo} No Path Found')
            
        else:
            
            path , length= PathFinder.aStar(self.__map, self.startxindex, self.endxindex, self.startyindex, self.endyindex )# find the a star path  , if no valid path, return none as path 
            if path is None:
                self.__screen.title(f'{self.__currentAlgo} No Path Found')#imform user in title screen if no path found 
                
            else:
                #instanciate the drone to walk the path 
                self.__drone  = Drone(self.startposx , self.startposy, self.startxindex  , self.startyindex , self.endxindex, self.endyindex,  self.__map , self.__squareDIM)
                # follow the path found by the path finder
                self.__drone.followpath(path, self.update_screen, reverse= True)
        
        self.__eventHandlerOn()#  allow user to change algo after path finding finish, import new file and restart pathfinding, by enabling event listener


    def update_screen(self, step):
        '''
        Step : params : number of step taken  so far by the algo
        '''
        self.__screen.title(f'Actions taken by {self.__currentAlgo}: {step}')
        

# Find all shortest path in a given grid
    def __allShortestPath(self):
        try:
            if self.__map is None:
                return
            # Switch algo to MPF
            self.__switchAlgo('MultiPathFinder')
            self.__eventHandlerOff()
            path , _ = PathFinder.aStar(self.__map, self.startxindex, self.endxindex, self.startyindex, self.endyindex ) # Use a* to find if there is solution
            # If no path, return prompt for no path
            if path is None:
                self.__screen.title(f'{self.__currentAlgo} No Path Found')
                self.__eventHandlerOn()
                self.__switchAlgo()
                return
            if self.__drone is not None:
                self.__drone.clear() # clear drawing of previous algo 
                self.__drone.ht() 
            multi_finder = MultiplePathFinder(self.__map, self.startxindex  , self.startyindex , self.endxindex, self.endyindex)
            self.__drone  = Drone(self.startposx , self.startposy, self.startxindex  , self.startyindex , self.endxindex, self.endyindex,  self.__map , self.__squareDIM)

            starting_depth = {(self.startxindex , self.startyindex): 0} # starting depth

            depth = multi_finder.bfs(starting_depth=starting_depth) # BFS

            for path in multi_finder.get_shortest_paths((self.startxindex , self.startyindex),(self.endxindex ,self.endyindex), depth):
                self.__drone.followpath(path=path, screenupdater=self.update_screen) #Follow the path devised by MultiPathFinder
                self.__drone.pencolor(*tuple(random.randint(0,254)/255 for _ in range(3)) ) # Set color palette
        except:
            self.__screen.title(f'{self.__currentAlgo} Unable to find path!')
        self.__eventHandlerOn()

    # Find the shortest path while passing every single drop off point
    def __findShortestWithDropOff(self):
        try:
            if self.__map is None:
                return
            # Switch algorithm to our bitmask algo
            self.__switchAlgo('BitMask DP Algorithm')
            self.__eventHandlerOff()

 
            if self.__drone is not None:
                self.__drone.clear() # clear drawing of previous algo 
                self.__drone.ht() 

            checkpoints = []
            if self.__map is None:
                return
            # Get all the checkpoints in a map
            for i in range(len(self.__map)):
                for j in range(len(self.__map[0])):
                    if self.__map[j,i] in [3,4,5]:
                        checkpoints.append((j,i))

            # Build the graph, and develop the shortest paths
            bm = BitMask(self.__map, checkpoints)
            self.__drone  = Drone(self.startposx , self.startposy, self.startxindex  , self.startyindex , self.endxindex, self.endyindex,  self.__map , self.__squareDIM)
            _ = bm.get_graph()
            path = bm.shortest_path((self.startxindex  , self.startyindex) , (self.endxindex, self.endyindex))
            if len(path) == 1: # If path is just starting position, return nothing found
                self.__screen.title(f'{self.__currentAlgo} No Path Found')
                self.__eventHandlerOn()
                return

            self.__drone.followpath(path=path, screenupdater=self.update_screen, reverse=False) #follow path
        except:
            self.__screen.title(f'{self.__currentAlgo} Unable to find path!')
        self.__eventHandlerOn() # set event handler back on
