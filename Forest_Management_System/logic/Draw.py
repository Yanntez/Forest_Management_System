import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from Forest_Management_System.logic.Health_status import HealthStatus

class Draw:
    @staticmethod
    def draw(forest):
        # 创建一个无向图
        G = nx.Graph()

        # 添加树作为节点
        for tree_id, tree in forest.trees.items():
            G.add_node(tree_id, tree=tree)

        # 添加路径作为边
        for path in forest.paths:
            G.add_edge(path.tree1.tree_id, path.tree2.tree_id, weight=path.distance)

        # 创建一个图形窗口
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.subplots_adjust(bottom=0.15)  # 调整子图布局以适应按钮

        # 为图形设置布局
        pos = nx.spring_layout(G, iterations=20)  # 增加迭代次数以优化布局

        health_color_map = {
            HealthStatus.HEALTHY: 'green',
            HealthStatus.INFECTED: 'red',
            HealthStatus.AT_RISK: 'orange'
        }

        # 绘制图形
        node_colors = [health_color_map.get(tree.health_status, 'gray') for tree_id, tree in forest.trees.items()]
        print(node_colors)
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

        # 定义按钮的回调函数
        def zoom_in(event):
            scale_factor = 1.1
            ax.set_xlim([x / scale_factor for x in ax.get_xlim()])
            ax.set_ylim([y / scale_factor for y in ax.get_ylim()])
            fig.canvas.draw_idle()

        def zoom_out(event):
            scale_factor = 1.1
            ax.set_xlim([x * scale_factor for x in ax.get_xlim()])
            ax.set_ylim([y * scale_factor for y in ax.get_ylim()])
            fig.canvas.draw_idle()

        def add_tree(event):
            scale_factor = 1.1
            ax.set_xlim([x * scale_factor for x in ax.get_xlim()])
            ax.set_ylim([y * scale_factor for y in ax.get_ylim()])
            fig.canvas.draw_idle()

        # 添加按钮
        ax_zoom_in = plt.axes([0.8, 0.05, 0.08, 0.05])
        ax_zoom_out = plt.axes([0.7, 0.05, 0.08, 0.05])
        btn_zoom_in = Button(ax_zoom_in, 'Zoom In')
        btn_zoom_out = Button(ax_zoom_out, 'Zoom Out')
        btn_zoom_in.on_clicked(zoom_in)
        btn_zoom_out.on_clicked(zoom_out)

        ax_add_tree = plt.axes([0.60, 0.05, 0.08, 0.05])
        btn_add_tree = Button(ax_add_tree, 'Add Tree')
        btn_add_tree.on_clicked(add_tree)

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
