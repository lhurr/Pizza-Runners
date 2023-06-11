from deque import Deque
class MultiplePathFinder:
    def __init__(self,grid, startx,starty,endx,endy):
        self.__grid = grid
        self.__startx = startx
        self.__starty = starty
        self.__endx = endx
        self.__endy = endy
    # Get shortest paths using DFS
    def get_shortest_paths(self,node, end, depth, path=None):
        if path is None:
            path = []
        path.append(node)
        if node == end:
            yield list(path)
        else:
            for neighbor in self.neighbors(node):
                if neighbor in depth and depth[neighbor] == depth[node]+1:
                    for sp in self.get_shortest_paths(neighbor, end, depth, path):
                        yield sp
        path.pop()
    # get the neighbour cells
    def neighbors(self,node):
        x, y = node
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            x2, y2 = x + dx, y + dy
            try:
                if self.__grid[x2,y2] == 0:
                    continue
            except IndexError:
                continue

            # if 0 <= x2 < len(self.__grid) and 0 <= y2 < len(self.__grid[0]):
            yield (x2, y2)
# BFS
    def bfs(self,starting_depth):
        nodes = Deque([(self.__startx, self.__starty)])
        while nodes:
            node = nodes.popleft()
            if node == (self.__endx, self.__endy):
                return starting_depth
                
            for neighbor in self.neighbors(node):
                if neighbor not in starting_depth:
                    starting_depth[neighbor] = starting_depth[node] + 1
                    nodes.append(neighbor)