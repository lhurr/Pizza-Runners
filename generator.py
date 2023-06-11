# P2112675 advance feature
from cartesiangrid import CartesianGrid
from random import choice 
from pprint import pprint
import random
from copy import deepcopy

class MazeGenerator():
    def __init__(self, height, width ) -> None:
        
        if not width  %2 ==1 :
            width += 1
            
        if not height %2 ==1:
            height += 1
            
        
        assert width >= 3
        assert height >= 3
        
        self.maze = CartesianGrid( [[0 for _ in range(width)] for _ in range(height)])# initialise maze with all building, the algorithm change the cells to road to bulid a proper maze later
        self.maze[0,0] =1
        pprint(self.maze)
        # pprint(self.maze)
        self.width = width
        self.height = height
        self.visited = set()
        self.visited.add((1,1)) 
        self.verticalmappings = {
            'N': ((lambda x, y , value: (x,y+value) ) , (lambda y : y < self.height -2) ),
            'S': ((lambda x, y , value: (x,y-value)  ) , (lambda y :y > 1 )),
           
        }
        
        self.horizontalmappings = {
            'E': ((lambda x, y , value: (x+value,y)  ) , (lambda x:x < self.width -2)),
            'W': ((lambda x, y , value: (x-value,y) ) , (lambda x:  x>1 ))
        }
    
    
    def create_maze(self):
        self.__recursive_create_maze(1,1)
        print(self.maze)
        maze =self.remove_walls(self.maze , 0.15  )
        maze, start, end = self.getstartend(self.maze)
        
        return maze

    def __recursive_create_maze(self , x,y ):
        self.maze[x,y] = 1 #make the current space a road
        # print(x,y)
        while True:
            notvisited = []
            for direction, (checkxy,checky) in self.verticalmappings.items():
                if checky(y) and checkxy(x,y, 2) not in self.visited:
                    notvisited.append(direction)
            
            for direction, (checkxy,checkx) in self.horizontalmappings.items():
                if checkx(x) and checkxy(x,y,2) not in self.visited:
                    notvisited.append(direction)
                    
            if len(notvisited) == 0:
                return 
            
            randomdirection = choice( notvisited)
            
            
            if randomdirection in {'N', 'S'}:
                
                nextposfunc ,_=self.verticalmappings[randomdirection]
            else:
                nextposfunc ,_=self.horizontalmappings[randomdirection]
            nextpos = nextposfunc(x,y,2)
            currpos = nextposfunc(x,y,1)
            
            self.maze[currpos] = 1
            
            self.visited.add(nextpos )
            self.__recursive_create_maze(*nextpos)
            
    def helpersetitem(self, maze, target, reverse = False):
        widthiter = range(1 , self.width) if not reverse else range(self.width-2, -1,-1)
        heightiter = range(1,self.height) if not reverse else range(self.height-2, -1,-1)
        for i in widthiter:
            for j in heightiter:
                if maze[i,j] == 1:
                    maze[i,j] = target
                    pos = (i,j)
                    return pos
    
    def getstartend(self,maze):
        startpos = ()
        startpos =self.helpersetitem(maze, 3)
        end  =self.helpersetitem(maze, 4 , True )
        
        
       
                
        return maze , startpos, end
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def remove_walls(self, maze, proportion):
        n_rows, n_cols = len(maze), len(maze[0])
        walls = [(i, j) for i in range(n_rows) for j in range(n_cols) if maze[i][j] == 0]
        n_walls_to_remove = int(proportion * len(walls))
        for _ in range(n_walls_to_remove):
            i, j = random.choice(walls)
            maze[i][j] = 1
            walls.remove((i, j))
        return maze

                



            
            
if __name__  == '__main__':
    generator = MazeGenerator(8,12)
    print(generator.verticalmappings['N'])
    
    generatedmaze = generator.create_maze()   
    
    pprint(generatedmaze)
    
                 
                
                 