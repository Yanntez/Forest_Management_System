from Forest_Management_System.entity.Forest import Forest
from Forest_Management_System.utils import load_dataset
from Forest_Management_System.entity.Path import Path
from Forest_Management_System.logic.Draw import Draw

# 定义文件路径
trees_file = 'assets/forest_management_dataset-trees.csv'
paths_file = 'assets/forest_management_dataset-paths.csv'

# 加载数据
forest = Forest()
load_dataset(forest, trees_file, paths_file)

# 显示森林状态
print(forest)
print("================================================")

# 查找保护区
conservation_areas = forest.find_conservation_areas()
print("保护区:", conservation_areas)

# 绘制森林图
Draw.draw(forest)

# 模拟传染传播
forest.simulate_infection_spread()



# 使用 Dijkstra 算法查找最短路径
start_tree_id = 3
end_tree_id = 5
shortest_distance = Path.dijkstra_shortest_path(forest, start_tree_id, end_tree_id)
print(f"Shortest distance from tree {start_tree_id} to tree {end_tree_id}: {shortest_distance}")
