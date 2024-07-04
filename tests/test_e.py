from tkinter import filedialog
import unittest
from unittest.mock import patch, mock_open, MagicMock
import csv
from enum import Enum, auto

# Define the HealthStatus enum
class HealthStatus(Enum):
    HEALTHY = auto()
    INFECTED = auto()
    AT_RISK = auto()

# Tree class definition
class Tree:
    def __init__(self, tree_id, species, age, health_status):
        self.tree_id = tree_id
        self.species = species
        self.age = age
        self.health_status = health_status if isinstance(health_status, HealthStatus) else None
    
    def __repr__(self):
        return f"Tree(ID: {self.tree_id}, Species: {self.species}, Age: {self.age}, Health Status: {self.health_status.name})"
    
    def __eq__(self, other):
        if isinstance(other, Tree):
            return self.tree_id == other.tree_id
        return False
    
    def __lt__(self, other):
        return self.age < other.age if isinstance(other, Tree) else NotImplemented

# Function definitions
def health_status_mapping(status_str):
    mapping = {
        'HEALTHY': HealthStatus.HEALTHY,
        'INFECTED': HealthStatus.INFECTED,
        'AT RISK': HealthStatus.AT_RISK
    }
    return mapping.get(status_str.upper(), None)

def load_dataset(forest, trees_file=None, paths_file=None):
    # Load trees
    if trees_file:
        with open(trees_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tree_id = int(row['tree_id'])
                species = row['species']
                age = int(row['age'])
                health_status = health_status_mapping(row['health_status'])
                tree = Tree(tree_id, species, age, health_status)
                forest.add_tree(tree)
   
    if paths_file:
        # Load paths
        with open(paths_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tree1_id = int(row['tree_1'])
                tree2_id = int(row['tree_2'])
                distance = float(row['distance'])
                forest.add_path(tree1_id, tree2_id, distance)

def choose_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="Select a CSV file"
    )
    if file_path:
        print(f"Selected file: {file_path}")
        return file_path
    else:
        print("No file selected")

# Test cases
class TestHealthStatusMapping(unittest.TestCase):
    def test_health_status_mapping(self):
        self.assertEqual(health_status_mapping('HEALTHY'), HealthStatus.HEALTHY)
        self.assertEqual(health_status_mapping('INFECTED'), HealthStatus.INFECTED)
        self.assertEqual(health_status_mapping('AT RISK'), HealthStatus.AT_RISK)
        self.assertIsNone(health_status_mapping('UNKNOWN'))

class TestTreeClass(unittest.TestCase):
    def test_tree_initialization(self):
        tree = Tree(1, 'oak', 100, HealthStatus.HEALTHY)
        self.assertEqual(tree.tree_id, 1)
        self.assertEqual(tree.species, 'oak')
        self.assertEqual(tree.age, 100)
        self.assertEqual(tree.health_status, HealthStatus.HEALTHY)

    def test_tree_representation(self):
        tree = Tree(1, 'oak', 100, HealthStatus.HEALTHY)
        self.assertEqual(repr(tree), "Tree(ID: 1, Species: oak, Age: 100, Health Status: HEALTHY)")

    def test_tree_equality(self):
        tree1 = Tree(1, 'oak', 100, HealthStatus.HEALTHY)
        tree2 = Tree(1, 'pine', 50, HealthStatus.INFECTED)
        tree3 = Tree(2, 'oak', 100, HealthStatus.HEALTHY)
        self.assertEqual(tree1, tree2)
        self.assertNotEqual(tree1, tree3)

    def test_tree_comparison(self):
        tree1 = Tree(1, 'oak', 100, HealthStatus.HEALTHY)
        tree2 = Tree(2, 'pine', 50, HealthStatus.INFECTED)
        self.assertTrue(tree2 < tree1)
        self.assertFalse(tree1 < tree2)

class TestLoadDataset(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='tree_id,species,age,health_status\n1,oak,100,HEALTHY\n2,pine,50,INFECTED')
    @patch('csv.DictReader')
    def test_load_trees(self, mock_dict_reader, mock_file):
        mock_dict_reader.return_value = csv.DictReader(['tree_id,species,age,health_status\n1,oak,100,HEALTHY\n2,pine,50,INFECTED\n'])
        forest = MagicMock()
        load_dataset(forest, 'fake_trees_file.csv', None)
        self.assertEqual(forest.add_tree.call_count, 2)
        calls = [call[0][0] for call in forest.add_tree.call_args_list]
        self.assertEqual(calls[0].tree_id, 1)
        self.assertEqual(calls[1].tree_id, 2)

    @patch('builtins.open', new_callable=mock_open, read_data='tree_1,tree_2,distance\n1,2,10.5\n2,3,15.0')
    @patch('csv.DictReader')
    def test_load_paths(self, mock_dict_reader, mock_file):
        mock_dict_reader.return_value = csv.DictReader(['tree_1,tree_2,distance\n1,2,10.5\n2,3,15.0\n'])
        forest = MagicMock()
        load_dataset(forest, None, 'fake_paths_file.csv')
        self.assertEqual(forest.add_path.call_count, 2)
        calls = [call[0] for call in forest.add_path.call_args_list]
        self.assertEqual(calls[0][0], 1)
        self.assertEqual(calls[0][1], 2)
        self.assertEqual(calls[0][2], 10.5)
        self.assertEqual(calls[1][0], 2)
        self.assertEqual(calls[1][1], 3)
        self.assertEqual(calls[1][2], 15.0)

    @patch('builtins.open', new_callable=mock_open, read_data='tree_id,species,age,health_status\n1,oak,100,HEALTHY\n2,pine,50,INFECTED\n')
    @patch('csv.DictReader')
    def test_load_dataset(self, mock_dict_reader, mock_file):
        mock_dict_reader.return_value = csv.DictReader(['tree_id,species,age,health_status\n1,oak,100,HEALTHY\n2,pine,50,INFECTED\n'])
        forest = MagicMock()
        load_dataset(forest, 'fake_trees_file.csv', 'fake_paths_file.csv')
        self.assertEqual(forest.add_tree.call_count, 2)
        self.assertEqual(forest.add_path.call_count, 0)

class TestChooseFile(unittest.TestCase):
    @patch('your_module.filedialog.askopenfilename')
    def test_choose_file(self, mock_askopenfilename):
        mock_askopenfilename.return_value = 'test.csv'
        file_path = choose_file()
        self.assertEqual(file_path, 'test.csv')

        mock_askopenfilename.return_value = ''
        file_path = choose_file()
        self.assertIsNone(file_path)

if __name__ == '__main__':
    unittest.main()
