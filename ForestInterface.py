import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 加载森林数据集
def load_forest_data(trees_file, paths_file):
    trees_df = pd.read_csv(trees_file)
    paths_df = pd.read_csv(paths_file)
    return trees_df, paths_df

# 创建无向图表示森林
def create_forest_graph(trees_df, paths_df):
    G = nx.Graph()

    # 添加树的节点
    for _, tree in trees_df.iterrows():
        G.add_node(tree['tree_id'], species=tree['species'], age=tree['age'], health_status=tree['health_status'])

    # 添加路径作为边
    for _, path in paths_df.iterrows():
        G.add_edge(path['tree_1'], path['tree_2'], distance=path['distance'])

    return G

# 绘制森林图
def draw_forest_graph(G):
    pos = nx.spring_layout(G)  # 使用Spring布局
    node_labels = {node: f"{G.nodes[node]['species']}\nAge: {G.nodes[node]['age']}\nHealth: {G.nodes[node]['health_status']}" for node in G.nodes()}
    edge_labels = {(edge[0], edge[1]): f"Distance: {G.edges[edge]['distance']}" for edge in G.edges()}

    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=1500, font_size=10, font_weight='bold', edge_color='gray', linewidths=1, font_color='black')
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title("Forest as an Undirected Graph")
    plt.show()

if __name__ == "__main__":
    # 数据集文件路径
    trees_file = "D:/xz/forest_management_dataset-trees.csv"
    paths_file = "D:/xz/forest_management_dataset-paths.csv"
    
    # 加载数据集
    trees_df, paths_df = load_forest_data(trees_file, paths_file)

    # 创建森林图
    forest_graph = create_forest_graph(trees_df, paths_df)

    # 绘制森林图
    draw_forest_graph(forest_graph)
