from data_loader import load_forest_data
from conservation_area import find_conservation_areas

# 加载森林数据
forest = load_forest_data('forest_management_dataset-trees.csv', 'forest_management_dataset-paths.csv')

# 任务1：识别保护区
conservation_areas = find_conservation_areas(forest)
for area in conservation_areas:
    print("保护区:", [tree.id for tree in area])
