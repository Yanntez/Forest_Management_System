import heapq


class Path:
    def __init__(self, tree1, tree2, distance):
        self.tree1 = tree1
        self.tree2 = tree2
        self.distance = distance
    
    def __repr__(self):
        return f"Path(Tree1: {self.tree1.tree_id}, Tree2: {self.tree2.tree_id}, Distance: {self.distance})"


    def dijkstra_shortest_path(self, start_tree_id, end_tree_id):
        distances = {tree_id: float('inf') for tree_id in self.trees}
        distances[start_tree_id] = 0
        priority_queue = [(0, start_tree_id)]
        parents = {tree_id: None for tree_id in self.trees}
        
        while priority_queue:
            current_distance, current_tree_id = heapq.heappop(priority_queue)
            
            if current_tree_id == end_tree_id:
                # 构建最短路径
                path = []
                while current_tree_id is not None:
                    path.append(current_tree_id)
                    current_tree_id = parents[current_tree_id]
                path.reverse()
                return distances[end_tree_id], path
            
            if current_distance > distances[current_tree_id]:
                continue
            
            for path in self.paths:
                if path.tree1.tree_id == current_tree_id:
                    neighbor_id = path.tree2.tree_id
                elif path.tree2.tree_id == current_tree_id:
                    neighbor_id = path.tree1.tree_id
                else:
                    continue
                
                distance = current_distance + path.distance
                
                if distance < distances[neighbor_id]:
                    distances[neighbor_id] = distance
                    parents[neighbor_id] = current_tree_id
                    heapq.heappush(priority_queue, (distance, neighbor_id))
        
        return float('inf'), []