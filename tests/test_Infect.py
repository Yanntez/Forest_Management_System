import unittest
from Forest_Management_System.logic.Health_status import HealthStatus
from Forest_Management_System.entity.Tree import Tree
from Forest_Management_System.entity.Path import  Path
from Forest_Management_System.logic.Infect import Infect 
from Forest_Management_System.entity.Forest import Forest  

class TestInfect(unittest.TestCase):
    
    def setUp(self):
        # 创建一些模拟的HealthStatus对象
        self.healthy = HealthStatus.HEALTHY
        self.infected = HealthStatus.INFECTED
        
        # 创建一些模拟的Tree对象
        self.treeA = Tree('A', 'Oak', 50, self.infected)
        self.treeB = Tree('B', 'Pine', 30, self.healthy)
        self.treeC = Tree('C', 'Birch', 20, self.healthy)
        self.treeD = Tree('D', 'Maple', 40, self.healthy)
        
        # 创建一些Path对象
        self.pathAB = Path(self.treeA, self.treeB, 1)
        self.pathBC = Path(self.treeB, self.treeC, 2)
        self.pathCD = Path(self.treeC, self.treeD, 1)
        self.pathBD = Path(self.treeB, self.treeD, 5)
        
        # 设置forest属性
        self.forest = Forest()
        self.forest.trees = {self.treeA.tree_id: self.treeA, self.treeB.tree_id: self.treeB, self.treeC.tree_id: self.treeC, self.treeD.tree_id: self.treeD}
        self.forest.paths = [self.pathAB, self.pathBC, self.pathCD, self.pathBD]
    
    def test_spread_infection(self):
        # 调用spread_infection方法
        Infect.spread_infection(self.forest)
        
        # 检查所有树的健康状态
        self.assertEqual(self.forest.trees['A'].health_status, HealthStatus.INFECTED)
        self.assertEqual(self.forest.trees['B'].health_status, HealthStatus.INFECTED)
        self.assertEqual(self.forest.trees['C'].health_status, HealthStatus.INFECTED)
        self.assertEqual(self.forest.trees['D'].health_status, HealthStatus.INFECTED)

if __name__ == '__main__':
    unittest.main()
