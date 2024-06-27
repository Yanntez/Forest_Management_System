import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt

from Forest_Management_System.entity.Forest import Forest

class Draw:
    @staticmethod
    def draw(forest, canvas):
        G = nx.Graph()

        for tree_id, tree in forest.trees.items():
            G.add_node(tree_id, tree=tree)

        for path in forest.paths:
            G.add_edge(path.tree1.tree_id, path.tree2.tree_id, weight=path.distance)

        fig, ax = plt.subplots(figsize=(12, 8))
        plt.subplots_adjust(bottom=0.2)

        pos = nx.spring_layout(G, iterations=20)

        nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_color='skyblue', node_size=5000)
        edges = nx.draw_networkx_edges(G, pos, ax=ax, edge_color='k')
        labels = nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight='bold')

        for node in G.nodes:
            tree = G.nodes[node]['tree']
            text_position = (pos[node][0], pos[node][1] - 0.05)
            ax.text(*text_position, f"{tree.species}\n{tree.health_status}",
                    fontsize=10, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.5))

        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

        def on_scroll(event):
            scale_factor = 1.1
            if event.button == 'up':
                scale_factor = 1 / scale_factor
            ax.set_xlim([x * scale_factor for x in ax.get_xlim()])
            ax.set_ylim([y * scale_factor for y in ax.get_ylim()])
            fig.canvas.draw_idle()

        fig.canvas.mpl_connect('scroll_event', on_scroll)
        
        canvas.draw()

def refresh(canvas, forest):
    plt.clf()  # 清除当前的图形
    Draw.draw(forest, canvas)

def main(forest):
    #forest = Forest()

    root = tk.Tk()
    root.title("Tree Graph")

    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    fig, ax = plt.subplots(figsize=(12, 8))
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    Draw.draw(forest, canvas)

    button = ttk.Button(frame, text="Refresh", command=lambda: refresh(canvas, forest))
    button.grid(row=1, column=0, pady=10)

    root.mainloop()

