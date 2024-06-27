from Forest_Management_System.entity.Forest import Forest
from Forest_Management_System.utils import load_dataset

# Load dataset
trees_file = 'assets/forest_management_dataset-trees.csv'
paths_file = 'assets/forest_management_dataset-paths.csv'

# Main script
forest = Forest()

load_dataset(forest, trees_file, paths_file)

# Display the forest
print(forest)


forest.display_graph()

