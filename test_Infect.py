import unittest
from collections import deque
from Forest_Management_System.entity.Health_status import HealthStatus
from unittest.mock import MagicMock
from Forest_Management_System.logic.Infect import Infect  # 假设您的实际文件名为 Infect.py，替换为实际的导入路径

class TestInfect(unittest.TestCase):

    def setUp(self):
        # 创建一个模拟的森林对象
        self.mock_forest = MagicMock()
        self.mock_forest.trees = {
            1: MagicMock(tree_id=1, health_status=HealthStatus.HEALTHY),
            2: MagicMock(tree_id=2, health_status=HealthStatus.INFECTED),
            3: MagicMock(tree_id=3, health_status=HealthStatus.HEALTHY),
            # 添加更多树木
        }
        self.mock_forest.paths = [
            MagicMock(tree1=self.mock_forest.trees[1], tree2=self.mock_forest.trees[2]),
            MagicMock(tree1=self.mock_forest.trees[2], tree2=self.mock_forest.trees[3]),
            # 添加更多路径
        ]

    def test_spread_infection(self):
        infect_simulation = Infect()

        # 在模拟森林对象上调用 spread_infection 方法
        infect_simulation.spread_infection(self.mock_forest)

        # TODO: 添加适当的断言来验证预期的感染传播结果
        # 例如，检查传染后树木的最终状态是否符合预期

if __name__ == '__main__':
    unittest.main()
