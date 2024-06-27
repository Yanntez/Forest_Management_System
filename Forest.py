from .Path import Path
from .Health_status import HealthStatus
from .Draw import Draw
import heapq

class Forest:
    def __init__(self):
        self.trees = {}
        self.paths = []
    
    def add_tree(self, tree):
        if tree.tree_id not in self.trees:
            self.trees[tree.tree_id] = tree
    
    def remove_tree(self, tree_id):
        if tree_id in self.trees:
            del self.trees[tree_id]
            self.paths = [path for path in self.paths if path.tree1.tree_id != tree_id and path.tree2.tree_id != tree_id]
    
    def add_path(self, tree1_id, tree2_id, distance):
        if tree1_id in self.trees and tree2_id in self.trees:
            path = Path(self.trees[tree1_id], self.trees[tree2_id], distance)
            self.paths.append(path)
    
    def remove_path(self, tree1_id, tree2_id):
        self.paths = [path for path in self.paths if not (path.tree1.tree_id == tree1_id and path.tree2.tree_id == tree2_id) and not (path.tree1.tree_id == tree2_id and path.tree2.tree_id == tree1_id)]
    
    def update_distance(self, tree1_id, tree2_id, new_distance):
        for path in self.paths:
            if (path.tree1.tree_id == tree1_id and path.tree2.tree_id == tree2_id) or (path.tree1.tree_id == tree2_id and path.tree2.tree_id == tree1_id):
                path.distance = new_distance
                break
    
    def update_health_status(self, tree_id, new_status):
        if tree_id in self.trees:
            tree = self.trees[tree_id]
            if isinstance(new_status, HealthStatus):
                tree.health_status = new_status
    
    def __repr__(self):
        result = "Forest:\n"
        result += "\n".join([str(tree) for tree in self.trees.values()])
        result += "\nPaths:\n"
        result += "\n".join([str(path) for path in self.paths])
        return result
    
    def display_graph(self):
        Draw.draw(self)

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
