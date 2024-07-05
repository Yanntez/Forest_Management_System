import unittest
from Forest_Management_System.entity.Forest import Forest
from Forest_Management_System.entity.Tree import Tree
from Forest_Management_System.entity.Health_status import HealthStatus
from unittest.mock import MagicMock, patch

class TestForest(unittest.TestCase):
    def setUp(self):
        self.forest = Forest()
        self.tree1 = Tree(1, "Oak", 50, HealthStatus.HEALTHY)
        self.tree2 = Tree(2, "Pine", 30, HealthStatus.INFECTED)
        self.tree3 = Tree(3, "Birch", 20, HealthStatus.AT_RISK)
        self.forest.add_tree(self.tree1)
        self.forest.add_tree(self.tree2)
        self.forest.add_tree(self.tree3)

    def test_add_tree(self):
        self.assertEqual(len(self.forest.trees), 3)
        new_tree = Tree(4, "Maple", 10, HealthStatus.HEALTHY)
        self.forest.add_tree(new_tree)
        self.assertEqual(len(self.forest.trees), 4)
        self.assertIn(new_tree.tree_id, self.forest.trees)

    def test_remove_tree(self):
        self.forest.remove_tree(1)
        self.assertEqual(len(self.forest.trees), 2)
        self.assertNotIn(1, self.forest.trees)

    def test_add_path(self):
        self.forest.add_path(1, 2, 5.0)
        self.assertEqual(len(self.forest.paths), 1)
        self.assertEqual(self.forest.paths[0].distance, 5.0)

    def test_remove_path(self):
        self.forest.add_path(1, 2, 5.0)
        self.forest.remove_path(1, 2)
        self.assertEqual(len(self.forest.paths), 0)

    def test_update_distance(self):
        self.forest.add_path(1, 2, 5.0)
        self.forest.update_distance(1, 2, 10.0)
        self.assertEqual(self.forest.paths[0].distance, 10.0)

    def test_update_health_status(self):
        self.forest.update_health_status(1, HealthStatus.INFECTED)
        self.assertEqual(self.forest.trees[1].health_status, HealthStatus.INFECTED)

    @patch('Forest_Management_System.logic.Infect.Infect.spread_infection')
    def test_simulate_infection_spread(self, mock_spread_infection):
        self.forest.simulate_infection_spread()
        mock_spread_infection.assert_called_with(self.forest)
        
    def test_repr(self):
        repr_str = repr(self.forest)
        self.assertIn("Forest:", repr_str)
        self.assertIn("Paths:", repr_str)

    def test_print_forest_status(self):
        with patch('builtins.print') as mock_print:
            self.forest.print_forest_status("2024-07-05")
            mock_print.assert_any_call("Time: 2024-07-05")
            mock_print.assert_any_call("Tree ID: 1, Health Status: HEALTHY")

if __name__ == '__main__':
    unittest.main()
