import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.path import Path
import networkx as nx
import matplotlib.pyplot as plt
from Forest_Management_System.entity.Forest import Forest
from Forest_Management_System.utils import load_dataset
from Forest_Management_System.entity.Tree import Tree
from Forest_Management_System.logic.Health_status import HealthStatus
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load dataset
trees_file = 'assets/forest_management_dataset-trees.csv'
paths_file = 'assets/forest_management_dataset-paths.csv'

# Main script
forest = Forest()
load_dataset(forest, trees_file, paths_file)

# Create the main window
root = tk.Tk()
root.title("Forest Management System")

# Create a frame for displaying the forest graph
graph_frame = tk.Frame(root)
graph_frame.pack(pady=10)

# Function to display/update the forest graph
def display_graph():
    global graph_canvas
    if 'graph_canvas' in globals():
        graph_canvas.get_tk_widget().pack_forget()
    
    G = nx.Graph()
    
    for tree_id, tree in forest.trees.items():
        G.add_node(tree_id, tree=tree)
    
    for path in forest.paths:
        G.add_edge(path.tree1.tree_id, path.tree2.tree_id, weight=path.distance)
    
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='k',
            node_size=700, font_size=10, font_weight='bold')
    
    # Display tree species and health status on nodes
    for node in G.nodes:
        tree = G.nodes[node]['tree']
        text_position = (pos[node][0], pos[node][1] - 0.05)
        plt.text(*text_position, f"{tree.species}\n{tree.health_status.name}",
                 fontsize=8, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.5))
    
    # Display edge weights
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.tight_layout()
    
    graph_canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_frame)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Function to add a tree
def add_tree():
    tree_id = simpledialog.askinteger("Input", "Enter tree ID:")
    species = simpledialog.askstring("Input", "Enter tree species:")
    age = simpledialog.askinteger("Input", "Enter tree age:")
    health_status = simpledialog.askstring("Input", "Enter tree health status (healthy, infected, at risk):")
    
    if tree_id is not None and species and age is not None and health_status:
        health_status_enum = HealthStatus[health_status.upper()]
        tree = Tree(tree_id, species, age, health_status_enum)
        forest.add_tree(tree)
        messagebox.showinfo("Success", "Tree added successfully!")
        display_graph()

# Function to remove a tree
def remove_tree():
    tree_id = simpledialog.askinteger("Input", "Enter tree ID to remove:")
    if tree_id is not None:
        forest.remove_tree(tree_id)
        messagebox.showinfo("Success", "Tree removed successfully!")
        display_graph()

# Create buttons for adding and removing trees
add_button = tk.Button(root, text="Add Tree", command=add_tree)
add_button.pack(pady=10)

remove_button = tk.Button(root, text="Remove Tree", command=remove_tree)
remove_button.pack(pady=10)

# Display the initial forest graph
display_graph()

# Run the GUI event loop
root.mainloop()
print(forest)


forest.display_graph()

forest.simulate_infection_spread()

 # Example of using Dijkstra's algorithm to find shortest path distance
start_tree_id = 3
end_tree_id = 5
shortest_distance = Path.dijkstra_shortest_path(forest,start_tree_id, end_tree_id)
print(f"Shortest distance from tree {start_tree_id} to tree {end_tree_id}: {shortest_distance}")