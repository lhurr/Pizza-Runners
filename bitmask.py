from deque import Deque
import functools
class BitMask:
    def __init__(self, grid, checkpoints) -> None:
        self.__grid = grid
        self.__checkpoints = checkpoints
    
    # Building of graph
    def get_graph(self):
        self.__graph = {}
        for chkpt in self.__checkpoints:
            self.__graph[chkpt] = {}
        for i in self.__checkpoints:
            for j in self.__checkpoints:
                if i != j:
                    self.__graph[i][j] = self.__get_checkpoint_distances(i, j)
        return self.__graph
    # Get the shortest distances between check points
    def __get_checkpoint_distances(self,point1, point2):
        queue = Deque([(point1, [])])
        visited = set()
        while queue:
            curr, path = queue.popleft()
            if curr in visited:
                continue
            visited.add(curr)
            x, y = curr
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbourX, neighbourY = x + dx, y + dy
                try:
                    #skip the current neighbour if the current neighbour is outside map (indexing error) or the neighbour is building
                    if self.__grid[neighbourX, neighbourY] == 0:
                        continue 
                except:
                    queue.append(((neighbourX, neighbourY), path + [(neighbourX, neighbourY)]))
                # if 0 <= neighbourX < len(self.__grid) and 0 <= neighbourY < len(self.__grid[0]) and self.__grid[neighbourX][neighbourY] != 0:
                if (neighbourX, neighbourY) == point2:
                    return path + [(neighbourX, neighbourY)]
                queue.append(((neighbourX, neighbourY), path + [(neighbourX, neighbourY)]))
        return []
    
    # Performs the bit masking
    @functools.lru_cache()
    def tsp(self,mask, position):
        if mask == (1 << len(self.__checkpoints)) - 1:
            return [self.__checkpoints[position]]
        res = []
        for i in range(len(self.__checkpoints)):
            if not (mask & (1 << i)):
                new_path = self.__graph[self.__checkpoints[position]][self.__checkpoints[i]] + self.tsp(mask | (1 << i), i)
                if len(new_path) > 0 and (len(res) == 0 or len(new_path) < len(res)):
                    res = new_path
        return res
    # Finds shortest paths
    def shortest_path(self, start, end):
        result = self.tsp(1 << self.__checkpoints.index(start), self.__checkpoints.index(start))
        return ([start] + result)[:-1]