import unittest
from unittest.mock import patch, mock_open
from Forest_Management_System.utils import health_status_mapping, load_dataset, choose_file
from Forest_Management_System.entity.Forest import Forest
from Forest_Management_System.entity.Tree import Tree
from Forest_Management_System.entity.Health_status import HealthStatus

class TestUtils(unittest.TestCase):
    
    def test_health_status_mapping(self):
        self.assertEqual(health_status_mapping("HEALTHY"), HealthStatus.HEALTHY)
        self.assertEqual(health_status_mapping("INFECTED"), HealthStatus.INFECTED)
        self.assertEqual(health_status_mapping("AT RISK"), HealthStatus.AT_RISK)
        self.assertIsNone(health_status_mapping("UNKNOWN"))

    @patch("builtins.open", new_callable=mock_open, read_data="tree_id,species,age,health_status\n1,Oak,50,HEALTHY\n2,Pine,30,INFECTED")
    def test_load_dataset_trees(self, mock_file):
        forest = Forest()
        trees_file = 'path/to/trees.csv'
        paths_file = None  # For this test, we're only loading trees
        load_dataset(forest, trees_file, paths_file)
        
        self.assertEqual(len(forest.trees), 2)
        self.assertIn(1, forest.trees)
        self.assertIn(2, forest.trees)
        self.assertEqual(forest.trees[1].species, "Oak")
        self.assertEqual(forest.trees[2].health_status, HealthStatus.INFECTED)

    @patch("builtins.open", new_callable=mock_open, read_data="tree_1,tree_2,distance\n1,2,5.0\n2,3,7.0")
    def test_load_dataset_paths(self, mock_file):
        forest = Forest()
        trees_file = None  # For this test, we're only loading paths
        paths_file = 'path/to/paths.csv'
        
        # Pre-populate the forest with trees
        forest.add_tree(Tree(1, "Oak", 50, HealthStatus.HEALTHY))
        forest.add_tree(Tree(2, "Pine", 30, HealthStatus.INFECTED))
        forest.add_tree(Tree(3, "Birch", 20, HealthStatus.AT_RISK))
        
        load_dataset(forest, trees_file, paths_file)
        
        self.assertEqual(len(forest.paths), 2)
        self.assertEqual(forest.paths[0].distance, 5.0)
        self.assertEqual(forest.paths[1].distance, 7.0)

    @patch("builtins.open", new_callable=mock_open, read_data="tree_id,species,age,health_status\n1,Oak,50,HEALTHY\n2,Pine,30,INFECTED\n")
    @patch("Forest_Management_System.utils.load_dataset")
    def test_load_dataset_combined(self, mock_load_dataset, mock_file):
        forest = Forest()
        trees_file = 'path/to/trees.csv'
        paths_file = 'path/to/paths.csv'
        mock_load_dataset(forest, trees_file, paths_file)
        
        self.assertEqual(len(forest.trees), 0)
        self.assertEqual(len(forest.paths), 0)
        
    @patch('tkinter.filedialog.askopenfilename')
    def test_choose_file(self, mock_askopenfilename):
        mock_askopenfilename.return_value = 'path/to/file.csv'
        file_path = choose_file()
        self.assertEqual(file_path, 'path/to/file.csv')

if __name__ == '__main__':
    unittest.main()
