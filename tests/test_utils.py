import unittest
from unittest.mock import patch, mock_open
from io import StringIO
import csv
from Forest_Management_System.entity.Tree import Tree
from Forest_Management_System.logic.Health_status import HealthStatus
from Forest_Management_System.utils import load_dataset, health_status_mapping

class MockForest:
    def __init__(self):
        self.trees = []
        self.paths = []

    def add_tree(self, tree):
        self.trees.append(tree)

    def add_path(self, tree1_id, tree2_id, distance):
        self.paths.append((tree1_id, tree2_id, distance))

class TestLoadDataset(unittest.TestCase):

    def setUp(self):
        self.mock_forest = MockForest()
        self.trees_csv = """tree_id,species,age,health_status
1,Oak,50,HEALTHY
2,Pine,30,INFECTED
3,Birch,20,AT RISK
"""
        self.paths_csv = """tree_1,tree_2,distance
1,2,10.5
2,3,20.75
1,3,15.0
"""

    def test_health_status_mapping(self):
        self.assertEqual(health_status_mapping('HEALTHY'), HealthStatus.HEALTHY)
        self.assertEqual(health_status_mapping('INFECTED'), HealthStatus.INFECTED)
        self.assertEqual(health_status_mapping('AT RISK'), HealthStatus.AT_RISK)
        self.assertIsNone(health_status_mapping('UNKNOWN'))

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_dataset_trees(self, mock_file):
        # Mock the file content for trees.csv
        mock_file.side_effect = [
            mock_open(read_data=self.trees_csv).return_value,
            mock_open(read_data=self.paths_csv).return_value
        ]

        load_dataset(self.mock_forest, "trees.csv", "paths.csv")

        self.assertEqual(len(self.mock_forest.trees), 3)
        self.assertEqual(self.mock_forest.trees[0].tree_id, 1)
        self.assertEqual(self.mock_forest.trees[0].species, "Oak")
        self.assertEqual(self.mock_forest.trees[0].age, 50)
        self.assertEqual(self.mock_forest.trees[0].health_status, HealthStatus.HEALTHY)

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_dataset_paths(self, mock_file):
        # Mock the file content for paths.csv
        mock_file.side_effect = [
            mock_open(read_data=self.trees_csv).return_value,
            mock_open(read_data=self.paths_csv).return_value
        ]

        load_dataset(self.mock_forest, "trees.csv", "paths.csv")

        self.assertEqual(len(self.mock_forest.paths), 3)
        self.assertEqual(self.mock_forest.paths[0], (1, 2, 10.5))
        self.assertEqual(self.mock_forest.paths[1], (2, 3, 20.75))
        self.assertEqual(self.mock_forest.paths[2], (1, 3, 15.0))

if __name__ == '__main__':
    unittest.main()
