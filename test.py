from enum import Enum, auto
import csv

# Enum and Tree Class
class HealthStatus(Enum):
    HEALTHY = auto()
    INFECTED = auto()
    AT_RISK = auto()

class Tree:
    def __init__(self, tree_id, species, age, health_status):
        self.tree_id = tree_id
        self.species = species
        self.age = age
        self.health_status = health_status if isinstance(health_status, HealthStatus) else None
    
    def __repr__(self):
        return f"Tree(ID: {self.tree_id}, Species: {self.species}, Age: {self.age}, Health Status: {self.health_status.name})"
    
    def __eq__(self, other):
        if isinstance(other, Tree):
            return self.tree_id == other.tree_id
        return False
    
    def __lt__(self, other):
        return self.age < other.age if isinstance(other, Tree) else NotImplemented

# Path Class
class Path:
    def __init__(self, tree1, tree2, distance):
        self.tree1 = tree1
        self.tree2 = tree2
        self.distance = distance
    
    def __repr__(self):
        return f"Path(Tree1: {self.tree1.tree_id}, Tree2: {self.tree2.tree_id}, Distance: {self.distance})"

# Forest Class
class Forest:
    def __init__(self):
        self.trees = {}
        self.paths = []
    
    def add_tree(self, tree):
        if tree.tree_id not in self.trees:
            self.trees[tree.tree_id] = tree
    
    def remove_tree(self, tree_id):
        if tree_id in self.trees:
            del self.trees[tree_id]
            self.paths = [path for path in self.paths if path.tree1.tree_id != tree_id and path.tree2.tree_id != tree_id]
    
    def add_path(self, tree1_id, tree2_id, distance):
        if tree1_id in self.trees and tree2_id in self.trees:
            path = Path(self.trees[tree1_id], self.trees[tree2_id], distance)
            self.paths.append(path)
    
    def remove_path(self, tree1_id, tree2_id):
        self.paths = [path for path in self.paths if not (path.tree1.tree_id == tree1_id and path.tree2.tree_id == tree2_id) and not (path.tree1.tree_id == tree2_id and path.tree2.tree_id == tree1_id)]
    
    def update_distance(self, tree1_id, tree2_id, new_distance):
        for path in self.paths:
            if (path.tree1.tree_id == tree1_id and path.tree2.tree_id == tree2_id) or (path.tree1.tree_id == tree2_id and path.tree2.tree_id == tree1_id):
                path.distance = new_distance
                break
    
    def update_health_status(self, tree_id, new_status):
        if tree_id in self.trees:
            tree = self.trees[tree_id]
            if isinstance(new_status, HealthStatus):
                tree.health_status = new_status
    
    def __repr__(self):
        result = "Forest:\n"
        result += "\n".join([str(tree) for tree in self.trees.values()])
        result += "\nPaths:\n"
        result += "\n".join([str(path) for path in self.paths])
        return result

# Helper function to map health status
def health_status_mapping(status_str):
    mapping = {
        'HEALTHY': HealthStatus.HEALTHY,
        'INFECTED': HealthStatus.INFECTED,
        'AT RISK': HealthStatus.AT_RISK
    }
    return mapping.get(status_str.upper(), None)

# Function to load dataset
def load_dataset(forest, trees_file, paths_file):
    # Load trees
    with open(trees_file, 'r') as file:
        #next(file)
        reader = csv.DictReader(file)
        print("Tree file columns:", reader.fieldnames)  # Print column names
 
        for row in reader:
            print(row['tree_id'])
            tree_id = int(row['tree_id'])
            species = row['species']
            age = int(row['age'])
            health_status = health_status_mapping(row['health_status'])
            tree = Tree(tree_id, species, age, health_status)
            forest.add_tree(tree)
   
   # Load paths
    with open(paths_file, 'r') as file:
        reader = csv.DictReader(file)
        print("Path file columns:", reader.fieldnames)  # Print column names
        for row in reader:
            tree1_id = int(row['tree_1'])
            tree2_id = int(row['tree_2'])
            distance = float(row['distance'])
            forest.add_path(tree1_id, tree2_id, distance)


# Main script
forest = Forest()

# Load dataset
trees_file = 'assets/forest_management_dataset-trees.csv'
paths_file = 'assets/forest_management_dataset-paths.csv'
load_dataset(forest, trees_file, paths_file)

# Display the forest
print(forest)
