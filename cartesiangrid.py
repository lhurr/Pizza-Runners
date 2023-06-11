# CLASS: DAAA2B02
# Member 1: Yee Hang (2112675)
# Member 2: Lim Hur (2112589)

class CartesianGrid(list):
    '''Implement a 2d array by subclassing list 
       Provides custom indexing that allows for specifying the x first then y, 
       unlike default 2d list , the rows on the bottom have lower index than rows above which is more inline with the turtle coordinate system
       Does not support negative indexing'''
    @staticmethod
    def __validate_index(index):
        #dont allow negative indexing as the equation self.__height - index-1 will result in negative index when the index is larger than the height which result in wrong cell returned 
        if index < 0:
            raise IndexError('negative indexing not supported')
        
    def __init__(self, *args):
        super().__init__(*args)# pass the iterable  to the list (parent class) constructor
        self.__height = len(self)# get the height 
     
    def __getitem__( self, index):
        ''''
        index: int or tuple, used to index one element by using tuple or index a whole row by using integer 
        '''
        #use of originalindex = (self.height - new index  - 1) to ensure the index passed in is in cartesian grid format
        if isinstance(index  , int ):# if the index is an integer , (only one index passed)
            newyindex =self.__height - index-1# calculate new y index
            # self.__validate_index(newyindex)# get the inner list (which represent a row) in the 2d list with the y index 
            return super().__getitem__(newyindex )#  get the item in the grid
        
        xindex , yindex = index 
        
        newyindex = self.__height - yindex-1# calculate the new index for y 
        self.__validate_index(newyindex) # validate whether x and y indexes are  negative
        self.__validate_index(xindex)
  # index the inner array with the calculated y index 
        return super().__getitem__(newyindex ).__getitem__(xindex)# get the element  
    
    def __setitem__(self,index , value):
        xindex , yindex = index 
        self[yindex][xindex ] = value # set the value to the grid with the specified y and x indices 
                
        