from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from Forest_Management_System.logic.Health_status import HealthStatus
from Forest_Management_System.entity.Path import Path
from Forest_Management_System.entity.Tree import Tree

class Draw:
    @staticmethod
    def draw(forest):

        def draw_graph():
            # 清除当前的图像
            ax.clear()

            # 创建一个无向图
            G = nx.Graph()

            # 添加树作为节点
            for tree_id, tree in forest.trees.items():
                G.add_node(tree_id, tree=tree)

            # 添加路径作为边
            for path in forest.paths:
                G.add_edge(path.tree1.tree_id, path.tree2.tree_id, weight=path.distance)

            # 为图形设置布局
            pos = nx.spring_layout(G, iterations=20)  # 增加迭代次数以优化布局

            health_color_map = {
                HealthStatus.HEALTHY: 'green',
                HealthStatus.INFECTED: 'red',
                HealthStatus.AT_RISK: 'orange'
            }

            handles = [plt.Line2D([0], [0], marker='o', color='w', label=label, markersize=10, markerfacecolor=color) for label, color in health_color_map.items()]
            ax.legend(handles=handles, loc='upper left', title="Legend")

            # 绘制图形
            node_colors = [health_color_map.get(tree.health_status, 'gray') for tree_id, tree in forest.trees.items()]
            nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=1000)
            edges = nx.draw_networkx_edges(G, pos, ax=ax, edge_color='k')
            labels = nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold')

            # 显示节点的树种和健康状况
            for node in G.nodes:
                tree = G.nodes[node]['tree']
                # 将文本固定在节点的正上方
                text_position = (pos[node][0], pos[node][1] - 0.05)  # Y坐标上稍微偏移
                ax.text(*text_position, f"{tree.species}\nAge:{tree.age}",
                        fontsize=10, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.5))

            # 显示边的权重
            edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

            fig.canvas.draw_idle()

        # 创建一个图形窗口
        fig, ax = plt.subplots(figsize=(12, 7))
        plt.subplots_adjust(bottom=0.15)  # 调整子图布局以适应按钮
        fig.canvas.manager.set_window_title('Forest Management System')
        draw_graph()  # 初次绘制图形

        # 定义按钮的回调函数
        def add_tree(event):
            tree_id = simpledialog.askinteger("Add", "Enter tree ID:")
            if tree_id is None:return
            species = simpledialog.askstring("Add", "Enter tree species:")
            if species is None:return
            age = simpledialog.askinteger("Add", "Enter tree age:")
            if age is None:return
            health_status = simpledialog.askstring("Add", "Enter tree health status (HEALTHY, INFECTED, AT_RISK):")
            if health_status is None:return
            if tree_id is not None and species and age is not None and health_status:
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
            if tree_id1 is None:return
            tree_id2 = simpledialog.askinteger("Path", "Enter tree ID2:")
            if tree_id2 is None:return
            distance = simpledialog.askinteger("Path", "Enter distance:")
            if tree_id1 and distance and tree_id2 is not None:
                forest.add_path( tree_id1, tree_id2, distance)
                draw_graph()
                messagebox.showinfo("Success", "Path Add successfully!")
            
        def remove_path(event):
            tree_id1 = simpledialog.askinteger("Path", "Enter tree ID1:")
            if tree_id1 is None:return
            tree_id2 = simpledialog.askinteger("Path", "Enter tree ID2:")
            if tree_id1 and tree_id2 is not None:
                forest.remove_path( tree_id1, tree_id2)
                draw_graph()
                messagebox.showinfo("Success", "Path Remove successfully!")

        def pathfinding(event):
            tree_id1 = simpledialog.askinteger("Path", "Enter tree ID1:")
            if tree_id1 is None:return
            tree_id2 = simpledialog.askinteger("Path", "Enter tree ID2:")
            if tree_id1 and tree_id2 is not None:
                way=Path.dijkstra_shortest_path(forest,tree_id1,tree_id2)
                print(Path.dijkstra_shortest_path(forest,tree_id1,tree_id2))
                if way[0] == float('inf'):
                    messagebox.showinfo("Dijkstra","No path found from the start to the end.")
                else:
                    messagebox.showinfo("Dijkstra", f"The shortest path length is:{way[0]}\nThe Path is:{way[1]}")

        def refresh(event):
            draw_graph()

        # 添加按钮
        ax_add_tree = plt.axes([0.1, 0.05, 0.08, 0.05])
        ax_remove_tree = plt.axes([0.2, 0.05, 0.08, 0.05])
        ax_add_path = plt.axes([0.3, 0.05, 0.08, 0.05])
        ax_remove_path = plt.axes([0.4, 0.05, 0.08, 0.05])
        ax_refresh = plt.axes([0.5, 0.05, 0.08, 0.05])
        ax_path_finding = plt.axes([0.6, 0.05, 0.08, 0.05])

        btn_add_tree = Button(ax_add_tree, 'Add Tree')
        btn_remove_tree = Button(ax_remove_tree, 'Remove Tree')
        btn_addpath = Button(ax_add_path, 'Add Path')
        btn_removepath = Button(ax_remove_path, 'Remove Path')
        btn_refresh = Button(ax_refresh, 'Refresh')
        btn_pathfinding = Button(ax_path_finding, 'Path Finding')

        btn_add_tree.on_clicked(add_tree)
        btn_remove_tree.on_clicked(remove_tree)
        btn_addpath.on_clicked(add_path)
        btn_removepath.on_clicked(remove_path)
        btn_refresh.on_clicked(refresh)
        btn_pathfinding.on_clicked(pathfinding)

        # 处理滚轮缩放
        def on_scroll(event):
            scale_factor = 1.1
            if event.button == 'up':
                scale_factor = 1 / scale_factor
            ax.set_xlim([x * scale_factor for x in ax.get_xlim()])
            ax.set_ylim([y * scale_factor for y in ax.get_ylim()])
            fig.canvas.draw_idle()

        fig.canvas.mpl_connect('scroll_event', on_scroll)

        # 显示图形
        plt.show()

