# Forest_Management_System
Efrei course assignment

#  Display
2024/6/28 version
You can check our feature design sources on this website
[Project 1 - Forest Management System](https://stealth-jodhpur-ff1.notion.site/Project-1-Forest-Management-System-f9f6a728bf814a8ea2b938bd10cf5993)
All of these functions have been implemented, and some of them have not been reflected in the interface yet. Only console output is supported, and we will improve it in the next few days.

Main Interface:
![2024/6/28 version](image.png)

Terminal:

![2](image-1.png)

# Forest Management System Mid-term Report

## Primary Data Structures
We utilize Python classes to represent individual trees in a forest and the paths between them. Each tree possesses attributes such as tree ID, species, age, and health status. The health status is defined using an enumeration type `HealthStatus`, ensuring the validity and consistency of status values.

- **Tree Node Representation**: Implemented with the `Tree` class, which includes methods to ensure `health_status` is an instance of the `HealthStatus` enumeration.
- **Path Representation**: The `Path` class represents weighted undirected paths between two trees in the forest.
- **Graph Representation**: The `Forest` class implements the data structure of the forest as an undirected graph, containing a collection of trees and a set of paths connecting these trees.

## Undirected Graph Drawing
The code uses the NetworkX and Matplotlib libraries to create a graphical representation of trees and their paths in a forest.
- It creates a graph object, adds tree nodes and path edges.
- Uses a spring layout to determine node positions.
- Colors nodes based on tree health status.
- Annotates detailed information.
- Finally, outputs the corresponding undirected graph of the forest.

## Infection Spread Simulation

We successfully implemented an infection spread simulation feature. This feature, based on the Breadth-First Search (BFS) algorithm, can accurately simulate the spread of infection among trees in a forest.

In each step of the simulation, it starts by identifying all currently infected trees. These trees become the starting points for the spread process. Initially, an infection queue is created and populated with the IDs of the initially infected trees. At the same time, a set is created to track visited trees, and the propagation rounds are initialized.

During the simulation, if the queue becomes empty, indicating that there are no more trees to process, the forest is rechecked to determine if there are any previously undiscovered sources of infection. If new infected trees are found, the simulation continues.

In each propagation round, the simulation will:
- Increase the propagation round count and print the current round.
- Remove a tree's ID from the queue and check all paths connected to it, looking for unvisited neighboring trees.
- If the neighboring trees are not yet infected, update their status to infected, add them to the visited set, and place them in the queue for the next round of processing.

The code uses class attributes to store the queue, the visited set, and the propagation rounds used during the process. This ensures continuity of state across multiple calls to the `spread_infection` method. If new sources of infection are discovered during the simulation, the propagation process is re-triggered to ensure all infections are identified and processed. If the queue is still empty at the end of a propagation round, it indicates that there are no more trees to process, and the simulation ends.

## Path Finding
This code implements Dijkstra's algorithm to calculate the shortest path between a given start tree and an end tree. By initializing the distances of all nodes to infinity and setting the distance of the start tree to 0, the algorithm uses a priority queue to progressively select the node with the current shortest distance and update the distances and parent nodes of its neighboring nodes.

- When the end tree is selected, the code backtracks to construct the complete shortest path and returns the shortest distance and the path. If no path is reachable, it returns infinity and an empty path.

## Graphical Interface
This code is a GUI application for a forest management system, utilizing the Tkinter library to create a user interface that allows users to manage forests interactively. The application provides the following main functionalities:

1. **User Interface Design**: Utilizes the Tkinter library to create a main window with buttons and dialogs for user interaction.
2. **Tree Management Features**: Includes buttons for adding and deleting trees, enabling users to perform corresponding actions by clicking these buttons. When adding a tree, a dialog prompts the user to enter relevant tree information. When deleting a tree, the user is prompted to enter the ID of the tree to be removed.

## Future Plans
Expand extra features, additional functionalities such as data analysis, graphical interaction, visualization of infection simulations, etc.
