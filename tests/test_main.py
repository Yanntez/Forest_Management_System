import unittest
from Forest import Forest
from Tree import Tree
from Path import Path
from Health_status import HealthStatus
from utils import load_dataset

class TestForestManagementSystem(unittest.TestCase):

    def setUp(self):
        self.forest = Forest()
        self.tree1 = Tree(1, 'Oak', 100, HealthStatus.HEALTHY)
        self.tree2 = Tree(2, 'Pine', 50, HealthStatus.INFECTED)
        self.tree3 = Tree(3, 'Birch', 70, HealthStatus.AT_RISK)
        self.forest.add_tree(self.tree1)
        self.forest.add_tree(self.tree2)

    def test_add_tree(self):
        self.forest.add_tree(self.tree3)
        self.assertIn(self.tree3.tree_id, self.forest.trees)

    def test_remove_tree(self):
        self.forest.remove_tree(self.tree1.tree_id)
        self.assertNotIn(self.tree1.tree_id, self.forest.trees)

    def test_add_path(self):
        self.forest.add_path(self.tree1.tree_id, self.tree2.tree_id, 10.5)
        self.assertEqual(len(self.forest.paths), 1)
        path = self.forest.paths[0]
        self.assertEqual(path.tree1, self.tree1)
        self.assertEqual(path.tree2, self.tree2)
        self.assertEqual(path.distance, 10.5)

    def test_remove_path(self):
        self.forest.add_path(self.tree1.tree_id, self.tree2.tree_id, 10.5)
        self.forest.remove_path(self.tree1.tree_id, self.tree2.tree_id)
        self.assertEqual(len(self.forest.paths), 0)

    def test_update_distance(self):
        self.forest.add_path(self.tree1.tree_id, self.tree2.tree_id, 10.5)
        self.forest.update_distance(self.tree1.tree_id, self.tree2.tree_id, 15.0)
        path = self.forest.paths[0]
        self.assertEqual(path.distance, 15.0)

    def test_update_health_status(self):
        self.forest.update_health_status(self.tree1.tree_id, HealthStatus.AT_RISK)
        self.assertEqual(self.tree1.health_status, HealthStatus.AT_RISK)

    def test_load_dataset(self):
        trees_file = 'path/to/your/trees_file.csv'
        paths_file = 'path/to/your/paths_file.csv'
        load_dataset(self.forest, trees_file, paths_file)
        self.assertGreater(len(self.forest.trees), 0)
        self.assertGreater(len(self.forest.paths), 0)

    def test_repr(self):
        self.forest.add_path(self.tree1.tree_id, self.tree2.tree_id, 10.5)
        repr_str = repr(self.forest)
        self.assertIn("Tree(ID: 1", repr_str)
        self.assertIn("Path(Tree1: 1", repr_str)

if __name__ == '__main__':
    unittest.main()
