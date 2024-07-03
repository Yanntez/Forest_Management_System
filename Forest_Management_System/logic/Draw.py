import copy
import threading
import time
import numpy as np
from tkinter import messagebox, simpledialog
import random as seednum
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button,CheckButtons
from Forest_Management_System.entity.Health_status import HealthStatus
from Forest_Management_System.entity.Path import Path
from Forest_Management_System.entity.Tree import Tree

class Draw:
    @staticmethod
    def draw(forest):
        global seeds
        seeds=0
        def draw_graph(mode):
            global seeds
            if seeds==0 :
                seeds = seednum.randint(1, 1000000)

            ax.clear()
            G = nx.Graph()
            for tree_id, tree in forest.trees.items():
                G.add_node(tree_id, tree=tree)
            for path in forest.paths:
                if mode==1: G.add_edge(path.tree1.tree_id, path.tree2.tree_id, weight=path.distance)
                else: G.add_edge(path.tree1.tree_id, path.tree2.tree_id, weight=1/path.distance)
            print(f"Now Graph Seed:{seeds}")
            


#  Strict layout code. If you sacrifice visualization for rigor, use this code
            if mode==1:
                pos = nx.kamada_kawai_layout(G, weight='weight')
                for (u, v, d) in G.edges(data=True):
                    distance = d['weight']
                    pos_u = pos[u]
                    pos_v = pos[v]
                    current_distance = np.linalg.norm(pos_u - pos_v)
                    scale_factor = distance / current_distance
                    pos[v] = pos[u] + (pos_v - pos_u) * scale_factor
            else: pos = nx.spring_layout(G,seed=seeds, iterations=20)



            health_color_map = {
                HealthStatus.HEALTHY: 'green',
                HealthStatus.INFECTED: 'red',
                HealthStatus.AT_RISK: 'orange'
            }

            handles = [plt.Line2D([0], [0], marker='o', color='w', label=label, markersize=10, markerfacecolor=color) for label, color in health_color_map.items()]
            ax.legend(handles=handles, loc='upper left', title="Legend")

            node_colors = [health_color_map.get(tree.health_status, 'gray') for tree_id, tree in forest.trees.items()]
            nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=1000)
            edges = nx.draw_networkx_edges(G, pos, ax=ax, edge_color='k')
            labels = nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold')

            edge_labels = {(path.tree1.tree_id, path.tree2.tree_id): path.distance for path in forest.paths}
            #edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
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

        fig, ax = plt.subplots(figsize=(12, 7))
        plt.subplots_adjust(bottom=0.15)
        fig.canvas.manager.set_window_title('Forest Management System')
        G, pos, nodes = draw_graph(mode=0)

        annot = ax.annotate("", xy=(0,0), xytext=(20,20),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        
                
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
                G, pos, nodes = draw_graph(check_buttons.get_status()[0])
                messagebox.showinfo("Success", "Tree added successfully!")

        def remove_tree(event):
            tree_id = simpledialog.askinteger("Remove", "Enter tree ID to remove:")
            if tree_id is not None:
                forest.remove_tree(tree_id)
                G, pos, nodes = draw_graph(check_buttons.get_status()[0])
                messagebox.showinfo("Success", "Tree removed successfully!")

        def add_path(event):
            tree_id1 = simpledialog.askinteger("Path", "Enter tree ID1:")
            if tree_id1 is None: return
            tree_id2 = simpledialog.askinteger("Path", "Enter tree ID2:")
            if tree_id2 is None: return
            distance = simpledialog.askinteger("Path", "Enter distance:")
            if tree_id1 and distance and tree_id2:
                forest.add_path(tree_id1, tree_id2, distance)
                G, pos, nodes = draw_graph(check_buttons.get_status()[0])
                messagebox.showinfo("Success", "Path added successfully!")

        def remove_path(event):
            tree_id1 = simpledialog.askinteger("Path", "Enter tree ID1:")
            if tree_id1 is None: return
            tree_id2 = simpledialog.askinteger("Path", "Enter tree ID2:")
            if tree_id1 and tree_id2:
                forest.remove_path(tree_id1, tree_id2)
                G, pos, nodes = draw_graph(check_buttons.get_status()[0])
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

        def simulate_multiple_infections(speed):
            forest_back=copy.deepcopy(forest.trees)
            while any(tree.health_status != HealthStatus.INFECTED for tree in forest.trees.values()):
                forest.simulate_infection_spread()
                G, pos, nodes = draw_graph(check_buttons.get_status()[0])
                for path in forest.paths:
                    if path.tree1.health_status == HealthStatus.INFECTED and path.tree2.health_status != HealthStatus.INFECTED:
                        time.sleep(path.distance * (1/speed))
                        break
                    elif path.tree2.health_status == HealthStatus.INFECTED and path.tree1.health_status != HealthStatus.INFECTED:
                        time.sleep(path.distance * (1/speed))
                        break
            forest.trees=forest_back
            print(forest_back)
            time.sleep(3)
            G, pos, nodes = draw_graph(check_buttons.get_status()[0])


        def spread_infection(event):
            speed = simpledialog.askinteger("Speed", "Enter tree Infection speed:")
            if speed is None: return
            thread = threading.Thread(target=simulate_multiple_infections,args=(speed,))
            thread.start()

        
        def conservation_areas(event):
            conservation_areas = forest.find_conservation_areas()
            area_count=0
            text=""
            for area in conservation_areas:
                area_count += 1
                if area_count != 1 : text += "\n"
                text += f"Conservation Areas {area_count}:{area}"
                
            messagebox.showinfo("Conservation Areas", text)

        def search_tree(event=None):
            search_species = simpledialog.askstring("Search", "Enter tree species:")
            if search_species is not None:
                found_trees = [tree for tree in forest.trees.values() if tree.species == search_species]
                if found_trees:
                    for tree in found_trees:
                        messagebox.showinfo("Search Result", f"Tree ID: {tree.tree_id}\nSpecies: {tree.species}\nAge: {tree.age}\nHealth: {tree.health_status.name}")
                else:
                    messagebox.showinfo("Search Result", "No trees found with the specified species.")

        def toggle_option(event):
                if (check_buttons.get_status()[0]==True):
                    G, pos, nodes = draw_graph(mode=1)
                else: G, pos, nodes = draw_graph(mode=0)

        def refresh(event):
            global seeds
            seeds=0
            G, pos, nodes = draw_graph(check_buttons.get_status()[0])
            

        ax_search = plt.axes([0.14, 0.91, 0.08, 0.05])
        ax_conservation_areas = plt.axes([0.24, 0.91, 0.13, 0.05])
        ax_path_file = plt.axes([0.39, 0.91, 0.13, 0.05])
        ax_tree_file = plt.axes([0.54, 0.91, 0.13, 0.05])
        ax_toggle = plt.axes([0.75, 0.91, 0.11, 0.05])  
        

        ax_add_tree = plt.axes([0.14, 0.05, 0.08, 0.05])
        ax_remove_tree = plt.axes([0.24, 0.05, 0.08, 0.05])
        ax_add_path = plt.axes([0.34, 0.05, 0.08, 0.05])
        ax_remove_path = plt.axes([0.44, 0.05, 0.09, 0.05])
        ax_refresh = plt.axes([0.55, 0.05, 0.08, 0.05])
        ax_path_finding = plt.axes([0.65, 0.05, 0.08, 0.05])
        ax_spread_infection = plt.axes([0.75, 0.05, 0.13, 0.05])


        btn_search = Button(ax_search, 'Search')
        btn_conservation_areas = Button(ax_conservation_areas, ' Conservation Areas')
        btn_path_file = Button(ax_path_file, 'Add Path From File')
        btn_tree_file = Button(ax_tree_file, 'Add Tree From File')
        check_buttons = CheckButtons(ax_toggle, ['Strict Mode'], [False]) 

        btn_add_tree = Button(ax_add_tree, 'Add Tree')
        btn_remove_tree = Button(ax_remove_tree, 'Remove Tree')
        btn_addpath = Button(ax_add_path, 'Add Path')
        btn_removepath = Button(ax_remove_path, 'Remove Path')
        btn_refresh = Button(ax_refresh, 'Refresh')
        btn_pathfinding = Button(ax_path_finding, 'Path Finding')
        btn_spread_infection = Button(ax_spread_infection, 'Infection Simulation')


        btn_search.on_clicked(search_tree)
        btn_conservation_areas.on_clicked(conservation_areas)
        btn_path_file.on_clicked(refresh)
        btn_tree_file.on_clicked(refresh)
        check_buttons.on_clicked(toggle_option)

        btn_add_tree.on_clicked(add_tree)
        btn_remove_tree.on_clicked(remove_tree)
        btn_addpath.on_clicked(add_path)
        btn_removepath.on_clicked(remove_path)
        btn_refresh.on_clicked(refresh)
        btn_pathfinding.on_clicked(pathfinding)
        btn_spread_infection.on_clicked(spread_infection)
        

        def on_scroll(event):
            scale_factor = 1.1
            if event.button == 'up':
                scale_factor = 1 / scale_factor
            ax.set_xlim([x * scale_factor for x in ax.get_xlim()])
            ax.set_ylim([y * scale_factor for y in ax.get_ylim()])
            fig.canvas.draw_idle()

        fig.canvas.mpl_connect('scroll_event', on_scroll)
        fig.canvas.mpl_connect('motion_notify_event', hover)

        plt.show()