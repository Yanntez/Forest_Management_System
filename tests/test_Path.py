import unittest
from heapq import heappush, heappop

from Forest_Management_System.entity.Tree import Tree
from Forest_Management_System.entity.Path import Path
from Forest_Management_System.entity.Health_status import HealthStatus  

class TestPath(unittest.TestCase):
    
    def setUp(self):
        # 创建一些模拟的HealthStatus对象
        self.healthy = HealthStatus.HEALTHY
        self.infected = HealthStatus.INFECTED
        
        # 创建一些模拟的Tree对象
        self.treeA = Tree('A', 'Oak', 50, self.healthy)
        self.treeB = Tree('B', 'Pine', 30, self.infected)
        self.treeC = Tree('C', 'Birch', 20, self.healthy)
        self.treeD = Tree('D', 'Maple', 40, self.infected)
        
        # 创建一些Path对象
        self.pathAB = Path(self.treeA, self.treeB, 1)
        self.pathAC = Path(self.treeA, self.treeC, 4)
        self.pathBC = Path(self.treeB, self.treeC, 2)
        self.pathBD = Path(self.treeB, self.treeD, 5)
        self.pathCD = Path(self.treeC, self.treeD, 1)
        
        # 设置trees和paths属性
        self.trees = [self.treeA, self.treeB, self.treeC, self.treeD]
        self.paths = [self.pathAB, self.pathAC, self.pathBC, self.pathBD, self.pathCD]
        
        # 使用一个实例来测试dijkstra_shortest_path方法
        self.path_instance = self.pathAB
        self.path_instance.trees = {tree.tree_id: tree for tree in self.trees}
        self.path_instance.paths = self.paths
    
    def test_dijkstra_shortest_path_A_to_D(self):
        # 测试从A到D的最短路径
        distance, path = self.path_instance.dijkstra_shortest_path('A', 'D')
        self.assertEqual(distance, 4)
        self.assertEqual(path, ['A', 'B', 'C', 'D'])
        
    def test_dijkstra_shortest_path_A_to_C(self):
        # 测试从A到C的最短路径
        distance, path = self.path_instance.dijkstra_shortest_path('A', 'C')
        self.assertEqual(distance, 3)
        self.assertEqual(path, ['A', 'B', 'C'])

if __name__ == '__main__':
    unittest.main()
