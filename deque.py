class Deque(list):
    """
    Deque class that subclasses list 
    Reasons:
    We need quicker pop operations from both the ends of the container, provides an O(1) time complexity for append and pop operations
    """
    def __init__(self, *args):
        super().__init__(*args)
    def popleft(self):
        # Pop left of the list, removing and returning first item
        if self.isEmpty():
            return None
        else:
            first = self[0]
            del self[0]
            return first
    def popright(self):
        # Pop right of a list, removing right most item
        if self.isEmpty():
            return None
        else:
            return super().pop()

    def append(self, item):
        # Append operation
        super().append(item)
    # String representation
    def __str__(self):
        return super().__str__()
    # Returns the size of deque
    def size(self):
        return super().__len__()
    # Returns boolean if deque is empty
    def isEmpty(self):
        return self.size() == 0
