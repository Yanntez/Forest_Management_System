import unittest
import tempfile
import csv
import os
from enum import Enum, auto
from Forest_Management_System.utils import load_dataset
class HealthStatus(Enum):
    HEALTHY = auto()
    INFECTED = auto()
    AT_RISK = auto()

def health_status_mapping(status_str):
    mapping = {
        'HEALTHY': HealthStatus.HEALTHY,
        'INFECTED': HealthStatus.INFECTED,
        'AT RISK': HealthStatus.AT_RISK
    }
    return mapping.get(status_str.upper(), None)

class Tree:
    def __init__(self, tree_id, species, age, health_status):
        self.tree_id = tree_id
        self.species = species
        self.age = age
        self.health_status = health_status if isinstance(health_status, HealthStatus) else None

class Forest:
    def __init__(self):
        self.trees = {}
        self.paths = []

    def add_tree(self, tree):
        self.trees[tree.tree_id] = tree

    def add_path(self, tree1_id, tree2_id, distance):
        self.paths.append((tree1_id, tree2_id, distance))


class TestLoadDataset(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()

        # Create a temporary trees file
        self.trees_file_path = os.path.join(self.test_dir.name, 'trees.csv')
        with open(self.trees_file_path, 'w', newline='') as trees_file:
            writer = csv.writer(trees_file)
            writer.writerow(['tree_id', 'species', 'age', 'health_status'])  # Header
            writer.writerow([1, 'Oak', 50, 'Healthy'])
            writer.writerow([2, 'Pine', 30, 'Infected'])
        
        # Create a temporary paths file
        self.paths_file_path = os.path.join(self.test_dir.name, 'paths.csv')
        with open(self.paths_file_path, 'w', newline='') as paths_file:
            writer = csv.writer(paths_file)
            writer.writerow(['tree_1', 'tree_2', 'distance'])  # Header
            writer.writerow([1, 2, 10.5])

        # Create a Forest instance
        self.forest = Forest()

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def test_load_dataset(self):
        # Call the load_dataset function
        load_dataset(self.forest, self.trees_file_path, self.paths_file_path)

        # Verify trees were loaded correctly
        self.assertEqual(len(self.forest.trees), 2)
        self.assertEqual(self.forest.trees[1].species, 'Oak')
        self.assertEqual(self.forest.trees[1].age, 50)
        self.assertNotEqual(self.forest.trees[1].health_status, HealthStatus.HEALTHY)
        self.assertEqual(self.forest.trees[2].species, 'Pine')
        self.assertEqual(self.forest.trees[2].age, 30)
        self.assertNotEqual(self.forest.trees[2].health_status, HealthStatus.INFECTED)

        # Verify paths were loaded correctly
        self.assertEqual(len(self.forest.paths), 1)
        self.assertIn((1, 2, 10.5), self.forest.paths)

if __name__ == '__main__':
    unittest.main()
