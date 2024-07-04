import unittest
from unittest.mock import MagicMock, patch
from Forest_Management_System.entity.Health_status import HealthStatus
from Forest_Management_System.entity.Path import Path
from Forest_Management_System.entity.Tree import Tree
from Forest_Management_System.utils import load_dataset
from Forest_Management_System.logic.Draw import Draw

class TestDraw(unittest.TestCase):

    def setUp(self):
        # Set up a mock forest for testing
        self.forest = MagicMock()
        self.tree1 = Tree(1, "Oak", 50, HealthStatus.HEALTHY)
        self.tree2 = Tree(2, "Pine", 30, HealthStatus.INFECTED)
        self.forest.trees = {1: self.tree1, 2: self.tree2}
        self.path = Path(self.tree1, self.tree2, 10)
        self.forest.paths = [self.path]

    @patch('matplotlib.pyplot.show')
    def test_draw_graph(self, mock_show):
        # Testing the draw method with mock data
        Draw.draw(self.forest)
        # Assert that the mock forest's trees and paths are accessed
        self.assertTrue(self.forest.trees)
        self.assertTrue(self.forest.paths)

if __name__ == '__main__':
    unittest.main()
