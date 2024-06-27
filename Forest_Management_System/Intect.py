from collections import deque
from Forest_Management_System.Health_status import HealthStatus

class Infect:
    @staticmethod
    def spread_infection(forest):
        print("Start simulating the contagion process(BFS):")
        # 初始化传染轮次
        spread_round = 0

        infected_trees = [tree.tree_id for tree_id, tree in forest.trees.items() if tree.health_status == HealthStatus.INFECTED]
        
        if not infected_trees:
            print("No infected trees found. No spread will occur.")
            return

        queue = deque(infected_trees)
        visited = set(infected_trees)

        while queue:
            # 每开始一轮新的传染，首先打印轮次标题
            spread_round += 1
            print(f"ROUND {spread_round}:")
            
            # 创建一个新队列以存储本轮传播的树
            next_round_queue = deque()

            while queue:
                current_tree_id = queue.popleft()  # 从队列中取出当前树的ID
                current_tree = forest.trees[current_tree_id]

                # 遍历森林中的所有路径，寻找相邻的树
                for path in forest.paths:
                    # 检查当前路径是否连接当前树和未访问的树
                    if (path.tree1.tree_id == current_tree_id and path.tree2.tree_id not in visited):
                        neighbor_id = path.tree2.tree_id
                    elif (path.tree2.tree_id == current_tree_id and path.tree1.tree_id not in visited):
                        neighbor_id = path.tree1.tree_id

                    # 如果邻居树未被访问且健康状况不是INFECTED，则进行感染
                    if neighbor_id not in visited and forest.trees[neighbor_id].health_status != HealthStatus.INFECTED:
                        visited.add(neighbor_id)
                        forest.trees[neighbor_id].health_status = HealthStatus.INFECTED
                        next_round_queue.append(neighbor_id)  # 为下一轮传播添加树
                        print(f"Infection spreads to Tree ID {neighbor_id} from Tree ID {current_tree_id}.")

            queue = next_round_queue  # 准备下一轮传播

        # 完成传播后，输出最终的森林状态
        print("Infection spread simulation complete. Final forest state:")
        for tree in forest.trees.values():
            print(tree)