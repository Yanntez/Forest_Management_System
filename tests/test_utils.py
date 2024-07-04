import unittest
from unittest.mock import patch, mock_open
import csv
from Forest_Management_System.utils import health_status_mapping, load_dataset  # Adjust the import according to your module structure
from Forest_Management_System.entity.Tree import Tree
from Forest_Management_System.entity.Health_status import HealthStatus
from Forest_Management_System.entity.Forest import Forest  # Assuming you have a Forest class


class TestHealthStatusMapping(unittest.TestCase):
    def test_health_status_mapping(self):
        self.assertEqual(health_status_mapping('HEALTHY'), HealthStatus.HEALTHY)
        self.assertEqual(health_status_mapping('INFECTED'), HealthStatus.INFECTED)
        self.assertEqual(health_status_mapping('AT RISK'), HealthStatus.AT_RISK)
        self.assertIsNone(health_status_mapping('UNKNOWN'))

class TestLoadDataset(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='tree_id,species,age,health_status\n1,Oak,50,HEALTHY\n2,Pine,30,INFECTED\n')
    def test_load_trees(self, mock_file):
        forest = Forest()
        trees_file = 'dummy_trees.csv'
        paths_file = 'dummy_paths.csv'

        with patch('csv.DictReader', return_value=csv.DictReader(mock_file())):
            load_dataset(forest, trees_file=trees_file, paths_file=paths_file)
        print(forest.trees)
        self.assertEqual(len(forest.trees), 2)
        self.assertEqual(forest.trees[1].tree_id, 1)
        self.assertEqual(forest.trees[1].species, 'Oak')
        self.assertEqual(forest.trees[1].age, 50)
        self.assertEqual(forest.trees[1].health_status, HealthStatus.HEALTHY)
        self.assertEqual(forest.trees[2].tree_id, 2)
        self.assertEqual(forest.trees[2].species, 'Pine')
        self.assertEqual(forest.trees[2].age, 30)
        self.assertEqual(forest.trees[2].health_status, HealthStatus.INFECTED)
    


if __name__ == '__main__':
    unittest.main()
