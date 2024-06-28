from Forest_Management_System.entity.Forest import Forest
from Forest_Management_System.utils import load_dataset
from Forest_Management_System.entity.Path import Path
from Forest_Management_System.logic.Draw import Draw

# Load dataset
trees_file = 'assets/forest_management_dataset-trees.csv'
paths_file = 'assets/forest_management_dataset-paths.csv'

# Main script
forest = Forest()

load_dataset(forest, trees_file, paths_file)

# Display the forest
print(forest)

#forest.remove_tree(3)
#forest.display_graph()
Draw.draw(forest)

forest.simulate_infection_spread()

 # Example of using Dijkstra's algorithm to find shortest path distance
start_tree_id = 3
end_tree_id = 5
shortest_distance = Path.dijkstra_shortest_path(forest,start_tree_id, end_tree_id)
print(f"Shortest distance from tree {start_tree_id} to tree {end_tree_id}: {shortest_distance}")