# CLASS: DAAA2B02
# Member 1: Yee Hang (2112675)
# Member 2: Lim Hur (2112589)
import re,os
class Util:
    """
    Utilities class that contains support for file validation.
    """
    @staticmethod
    def read_file(path: str):
        '''
        Validation of user file input
        Attribute: 
        :param path: Path to map

        :return file content
        '''
        
        try:
            if not path.endswith('.txt'):#ensure file path ends in txt
                return 'Only .txt files are accepted', 1 
            assert not bool(re.match(r'[\\/*?:"<>|]', path)), 'Filename with illegal special characters! Please renter the filepath to the map' # ensure there are no special characters
            
            with open(path) as r:
                content = r.read()
            assert content.count('e') == 1, 'Please enter one end point! Please renter the filepath to the map'# ensure only one start 
            assert content.count('s') == 1, 'Please enter one start point! Please renter the filepath to the map'
            if len(content.strip()) ==0 :#
                return 'File is empty' , 1 
                

        except FileNotFoundError:# if file does not exist , imform the user
            return f'File {path} does not exist. Please try again', 1
        except OSError:
            return f'Error, OS could not read the file: {path}. Please try again' , 1 
        except AttributeError as e:
            return f'Please enter a valid file', 1
        except Exception as e:
            return f'{e}', 1

        return content , 0  
    
    @staticmethod 
    def check_jagged_array(arr):
        '''
        Validation of user file input (check jaggered arrays, ensures the map has the same number of columns for all the rows )
        Attribute: 
        :param arr: (2d array represented by nested list )

        :return boolean
        '''
        initial_len = len(arr[0] )# get the length of first inner list  
        
        
        for l in arr:# loop through the inner array
            if len(l) != initial_len:# if the length of the inner list  in current iteration is not equal to the initial list, means the array is jagged 
                return True    # return true to the gui for alert the user 
            
        return False# the array is not jagged 
