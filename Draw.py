from tkinter import Tk, StringVar, OptionMenu, messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from Forest_Management_System.logic.Health_status import HealthStatus
from Forest_Management_System.entity.Path import Path
from Forest_Management_System.entity.Tree import Tree
from Forest_Management_System.entity.Forest import Forest

class Draw:
    @staticmethod
    def draw(forest):
        def draw_graph(filtered_trees=None):
            ax.clear()
            G = nx.Graph()
            trees = forest.trees if filtered_trees is None else filtered_trees
            for tree_id, tree in trees.items():
                G.add_node(tree_id, tree=tree)
            for path in forest.paths:
                if path.tree1.tree_id in trees and path.tree2.tree_id in trees:
                    G.add_edge(path.tree1.tree_id, path.tree2.tree_id, weight=path.distance)
            pos = nx.spring_layout(G, iterations=20)

            health_color_map = {
                HealthStatus.HEALTHY: 'green',
                HealthStatus.INFECTED: 'red',
                HealthStatus.AT_RISK: 'orange'
            }

            handles = [plt.Line2D([0], [0], marker='o', color='w', label=label, markersize=10, markerfacecolor=color) for label, color in health_color_map.items()]
            ax.legend(handles=handles, loc='upper left', title="Legend")

            node_colors = [health_color_map.get(tree.health_status, 'gray') for tree_id, tree in trees.items()]
            nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=1000)
            edges = nx.draw_networkx_edges(G, pos, ax=ax, edge_color='k')
            labels = nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold')

            edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

            fig.canvas.draw_idle()

            return G, pos, nodes

        def update_annot(ind):
            node = ind['ind'][0]
            tree_id = list(G.nodes)[node]
            tree = G.nodes[tree_id]['tree']
            pos_node = pos[tree_id]
            annot.xy = pos_node
            text = f"Species: {tree.species}\nAge: {tree.age}\nHealth: {tree.health_status.name}"
            annot.set_text(text)
            annot.get_bbox_patch().set_alpha(0.4)
            annot.set_visible(True)
            fig.canvas.draw_idle()

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == ax:
                cont, ind = nodes.contains(event)
                if cont:
                    update_annot(ind)
                else:
                    if vis:
                        annot.set_visible(False)
                        fig.canvas.draw_idle()

        def search_tree(event=None):
            search_species = simpledialog.askstring("Search", "Enter tree species:")
            if search_species is not None:
                found_trees = [tree for tree in forest.trees.values() if tree.species == search_species]
                if found_trees:
                    for tree in found_trees:
                        messagebox.showinfo("Search Result", f"Tree ID: {tree.tree_id}\nSpecies: {tree.species}\nAge: {tree.age}\nHealth: {tree.health_status.name}")
                else:
                    messagebox.showinfo("Search Result", "No trees found with the specified species.")

        def add_tree(event):
            tree_id = simpledialog.askinteger("Add", "Enter tree ID:")
            if tree_id is None: return
            species = simpledialog.askstring("Add", "Enter tree species:")
            if species is None: return
            age = simpledialog.askinteger("Add", "Enter tree age:")
            if age is None: return
            health_status = simpledialog.askstring("Add", "Enter tree health status (HEALTHY, INFECTED, AT_RISK):")
            if health_status is None: return
            if tree_id and species and age and health_status:
                health_status_enum = HealthStatus[health_status.upper()]
                tree = Tree(tree_id, species, age, health_status_enum)
                forest.add_tree(tree)
                draw_graph()
                messagebox.showinfo("Success", "Tree added successfully!")

        def remove_tree(event):
            tree_id = simpledialog.askinteger("Remove", "Enter tree ID to remove:")
            if tree_id is not None:
                forest.remove_tree(tree_id)
                draw_graph()
                messagebox.showinfo("Success", "Tree removed successfully!")

        def add_path(event):
            tree_id1 = simpledialog.askinteger("Path", "Enter tree ID1:")
            if tree_id1 is None: return
            tree_id2 = simpledialog.askinteger("Path", "Enter tree ID2:")
            if tree_id2 is None: return
            distance = simpledialog.askinteger("Path", "Enter distance:")
            if tree_id1 and distance and tree_id2:
                forest.add_path(tree_id1, tree_id2, distance)
                draw_graph()
                messagebox.showinfo("Success", "Path added successfully!")

        def remove_path(event):
            tree_id1 = simpledialog.askinteger("Path", "Enter tree ID1:")
            if tree_id1 is None: return
            tree_id2 = simpledialog.askinteger("Path", "Enter tree ID2:")
            if tree_id1 and tree_id2:
                forest.remove_path(tree_id1, tree_id2)
                draw_graph()
                messagebox.showinfo("Success", "Path removed successfully!")

        def pathfinding(event):
            tree_id1 = simpledialog.askinteger("Path", "Enter tree ID1:")
            if tree_id1 is None: return
            tree_id2 = simpledialog.askinteger("Path", "Enter tree ID2:")
            if tree_id1 and tree_id2:
                way = Path.dijkstra_shortest_path(forest, tree_id1, tree_id2)
                if way[0] == float('inf'):
                    messagebox.showinfo("Dijkstra", "No path found from the start to the end.")
                else:
                    messagebox.showinfo("Dijkstra", f"The shortest path length is: {way[0]}\nThe Path is: {way[1]}")

        def refresh(event=None):
            draw_graph()

        def filter_trees(event=None):
            selected_species = simpledialog.askstring("Filter", "Enter tree species to filter:")
            if selected_species is None:
                return

            if selected_species == 'All':
                filtered_trees = None  # Show all trees
            else:
                filtered_trees = {tree.tree_id: tree for tree in forest.trees.values() if tree.species == selected_species}

            draw_graph(filtered_trees)

        # Initialize Tkinter root window
        root = Tk()
        root.withdraw()  # Hide the root window

        fig, ax = plt.subplots(figsize=(12, 7))
        plt.subplots_adjust(bottom=0.25)
        fig.canvas.manager.set_window_title('Forest Management System')
        G, pos, nodes = draw_graph()

        annot = ax.annotate("", xy=(0,0), xytext=(20,20),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        ax_add_tree = plt.axes([0.1, 0.05, 0.08, 0.05])
        ax_remove_tree = plt.axes([0.2, 0.05, 0.08, 0.05])
        ax_add_path = plt.axes([0.3, 0.05, 0.08, 0.05])
        ax_remove_path = plt.axes([0.4, 0.05, 0.08, 0.05])
        ax_refresh = plt.axes([0.5, 0.05, 0.08, 0.05])
        ax_path_finding = plt.axes([0.6, 0.05, 0.08, 0.05])
        ax_search = plt.axes([0.7, 0.05, 0.08, 0.05])
        ax_filter = plt.axes([0.8, 0.05, 0.08, 0.05])

        btn_add_tree = Button(ax_add_tree, 'Add Tree')
        btn_remove_tree = Button(ax_remove_tree, 'Remove Tree')
        btn_addpath = Button(ax_add_path, 'Add Path')
        btn_removepath = Button(ax_remove_path, 'Remove Path')
        btn_refresh = Button(ax_refresh, 'Refresh')
        btn_pathfinding = Button(ax_path_finding, 'Path Finding')
        btn_search = Button(ax_search, 'Search')
        btn_filter = Button(ax_filter, 'Filter')

        btn_add_tree.on_clicked(add_tree)
        btn_remove_tree.on_clicked(remove_tree)
        btn_addpath.on_clicked(add_path)
        btn_removepath.on_clicked(remove_path)
        btn_refresh.on_clicked(refresh)
        btn_pathfinding.on_clicked(pathfinding)
        btn_search.on_clicked(search_tree)
        btn_filter.on_clicked(filter_trees)

        species_list = ['All'] + list(set([tree.species for tree in forest.trees.values()]))
        species_var = StringVar(root)
        species_var.set('All')
        species_menu = OptionMenu(root, species_var, *species_list)
        species_menu.pack()

        plt.connect('motion_notify_event', hover)
        plt.show()

if __name__ == '__main__':
    forest = Forest()  # Assuming Forest is properly initialized
    Draw.draw(forest)
