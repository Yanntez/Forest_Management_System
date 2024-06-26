import csv
from .Tree import Tree
from .Forest import Forest
from .Health_status import HealthStatus


def health_status_mapping(status_str):
    mapping = {
        'HEALTHY': HealthStatus.HEALTHY,
        'INFECTED': HealthStatus.INFECTED,
        'AT RISK': HealthStatus.AT_RISK
    }
    return mapping.get(status_str.upper(), None)

def load_dataset(forest, trees_file, paths_file):
    tree_fieldnames = ['tree_id', 'species', 'age', 'health_status']
    path_fieldnames = ['tree_1', 'tree_2', 'distance']
    
    # Load trees
    with open(trees_file, 'r') as file:
        reader = csv.DictReader(file, fieldnames=tree_fieldnames)
        next(reader)  # Skip header row
        for row in reader:
            tree_id = int(row['tree_id'])
            species = row['species']
            age = int(row['age'])
            health_status = health_status_mapping(row['health_status'])
            tree = Tree(tree_id, species, age, health_status)
            forest.add_tree(tree)
    
    # Load paths
    with open(paths_file, 'r') as file:
        reader = csv.DictReader(file, fieldnames=path_fieldnames)
        next(reader)  # Skip header row
        for row in reader:
            tree1_id = int(row['tree_1'])
            tree2_id = int(row['tree_2'])
            distance = float(row['distance'])
            forest.add_path(tree1_id, tree2_id, distance)



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


