from Forest_Management_System.Forest import Forest
from Forest_Management_System.utils import load_dataset

# Load dataset
trees_file = 'assets/forest_management_dataset-trees.csv'
paths_file = 'assets/forest_management_dataset-paths.csv'

# Main script
def main():
    # Create a forest instance
    forest = Forest()

    # Load dataset into the forest
    load_dataset(forest, trees_file, paths_file)

    # Display the forest structure
    print(forest)

    # Example of using Dijkstra's algorithm to find shortest path distance
    start_tree_id = 2
    end_tree_id = 5
    shortest_distance = forest.dijkstra_shortest_path(start_tree_id, end_tree_id)
    print(f"Shortest distance from tree {start_tree_id} to tree {end_tree_id}: {shortest_distance}")


    # Display the forest graph
    forest.display_graph()

if __name__ == "__main__":
    main()