import csv


from Forest_Management_System.utils import health_status_mapping

from Forest_Management_System.Forest import Forest
from Forest_Management_System.Tree import Tree
from Forest_Management_System.Path import Path
from Forest_Management_System.Health_status import HealthStatus




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



