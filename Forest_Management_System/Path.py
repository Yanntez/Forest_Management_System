from .Tree import Tree

class Path:
    def __init__(self, tree1, tree2, distance):
        self.tree1 = tree1
        self.tree2 = tree2
        self.distance = distance
    
    def __repr__(self):
        return f"Path(Tree1: {self.tree1.tree_id}, Tree2: {self.tree2.tree_id}, Distance: {self.distance})"
