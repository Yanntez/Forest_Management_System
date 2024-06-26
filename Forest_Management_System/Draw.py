# draw.py
import networkx as nx
import matplotlib.pyplot as plt

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
        plt.figure(figsize=(12, 12))  # 可以调整图形窗口的大小

        # 为图形设置布局
        pos = nx.spring_layout(G, iterations=20)  # 增加迭代次数以优化布局

        # 绘制图形
        nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='k',
                 node_size=7000, font_size=12, font_weight='bold')

        # 显示节点的树种和健康状况
        for node in G.nodes:
            tree = G.nodes[node]['tree']
            # 将文本固定在节点的正上方
            text_position = (pos[node][0], pos[node][1] - 0.05)  # Y坐标上稍微偏移
            plt.text(*text_position, f"{tree.species}\n{tree.health_status.name}",
                     fontsize=10, ha='center', va='top', bbox=dict(facecolor='white', alpha=0.5))

        # 显示边的权重
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # 调整布局以适应标签
        plt.tight_layout()

        # 显示图形
        plt.show()