from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from Forest_Management_System.logic.Health_status import HealthStatus
from Forest_Management_System.entity.Forest import Forest
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
                ax.text(*text_position, f"{tree.species}\n{tree.health_status.name}",
                        fontsize=10, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.5))

            # 显示边的权重
            edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

            fig.canvas.draw_idle()

        # 创建一个图形窗口
        fig, ax = plt.subplots(figsize=(15, 9))
        plt.subplots_adjust(bottom=0.15)  # 调整子图布局以适应按钮

        draw_graph()  # 初次绘制图形

        # 定义按钮的回调函数
        def add_tree(event):
            tree_id = simpledialog.askinteger("Add", "Enter tree ID:")
            species = simpledialog.askstring("Add", "Enter tree species:")
            age = simpledialog.askinteger("Add", "Enter tree age:")
            health_status = simpledialog.askstring("Add", "Enter tree health status (HEALTHY, INFECTED, AT_RISK):")
    
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

        def refresh(event):
            draw_graph()

        # 添加按钮
        ax_add_tree = plt.axes([0.1, 0.05, 0.08, 0.05])
        ax_remove_tree = plt.axes([0.2, 0.05, 0.08, 0.05])
        ax_refresh = plt.axes([0.3, 0.05, 0.08, 0.05])

        btn_add_tree = Button(ax_add_tree, 'Add Tree')
        btn_remove_tree = Button(ax_remove_tree, 'Remove Tree')
        btn_refresh = Button(ax_refresh, 'Refresh')

        btn_add_tree.on_clicked(add_tree)
        btn_remove_tree.on_clicked(remove_tree)
        btn_refresh.on_clicked(refresh)
        

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

# 测试代码
# forest = Forest()  # 假设你已经有一个Forest实例
# Draw.draw(forest)
