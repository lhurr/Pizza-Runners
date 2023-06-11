# CLASS: DAAA2B02
# Member 1: Yee Hang (2112675)
# Member 2: Lim Hur (2112589)

import turtle as t

class TurtleGrid(t.Turtle):
    """Turtle pen that draws turtle grid"""
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # Inherit from parent class - turtle.Turtle
        # Defines the mapping for each block type 
        # 0 (building) : Grey Color; 1 (open road): White; 3 (Start): Light green; 4 : light blue
        self.__mapping  = {
            0: '#C3C3C3',  # Grey color
            1 : 'white',  #White color
            3: '#7EFF7E' , #Light green
            4: '#7FFFFE', # Light blue
            5: '#00008b'
        }
        
    # Method to fill blocks, based on color
    def draw_fill_sqaure(self,color,size_per_square):
        """
        Draw filled square
        Params: 
        :param color: Color of block
        :param size_per_square: Dimension of each square
        :return 
        """
        self.color(color) #Set pen color and color to color
        self.begin_fill()   # Begin filling a square
        for _ in range(4):  # Draw a square with 4 sides
          self.forward(size_per_square)
          self.left(90)     # Make a 90 degree left turn
        self.end_fill()     # End the fill
        
    def draw_sqaure(self,color, size_per_square):
        """
        Draw the square outline
        Params: 
        :param color: Color of block
        :param size_per_square: Dimension of each square
        :return
        """
        self.color(color) # Set color of pen to black by default
        # Draw square
        for _ in range(4):
            self.forward(size_per_square)   # Move forward
            self.left(90)   # Make a 90 degree left turn

    def draw_maze(self, maze, size_per_square: int, startposx, startposy):
        """
        Draw the maze
        Params: 
        :param maze: 2D cartesian grid, filled with 0, 1, 3 or 4
        :param size_per_square: 
        :param startposx: 
        :return the START x, y coordinates and END x,y coordinates of the maze
        """
        width = len(maze[0])    #Get the width of the grid/maze
        height = len(maze)    # Get the height of grid/maze

        # Drawing of the entire grid
        for row in range(height-1, -1 , -1):    # Loop through row
            for col in range(width):    # Loop through column
                point = maze[col, row]    # Get the type of point of based on row and column - whether it is an open path, building, start or end
                self.goto(startposx + col*size_per_square,startposy+ row*size_per_square)    # To centralise the whole maze
                self.pendown()   # Pendown so as to draw the square outline and fill its color
                # Drawing of individual grid cells
                self.draw_fill_sqaure( self.__mapping[point], size_per_square)
                self.draw_sqaure('black', size_per_square)

                if point == 3:
                    # get x and y coordinates of starting point                    
                    startxindex,startyindex = col, row 
                elif point == 4:
                    # get x and y coordinates of ending point 
                    endxindex , endyindex = col, row
                self.penup() # Pen up when moving to next col
        self.hideturtle() # Make turtle invinsible
        return startxindex , startyindex , endxindex ,endyindex