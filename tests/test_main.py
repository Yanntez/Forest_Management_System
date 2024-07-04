import unittest
from unittest.mock import patch, mock_open
from Forest_Management_System.entity.Forest import Forest
from Forest_Management_System.utils import load_dataset
from Forest_Management_System.logic.Draw import Draw

class TestForestManagementSystem(unittest.TestCase):
    def setUp(self):
        self.forest = Forest()

    @patch("builtins.open", new_callable=mock_open, read_data="sample tree data")
    @patch("Forest_Management_System.utils.load_dataset")
    def test_load_dataset(self, mock_load_dataset, mock_file):
        # Test loading dataset
        trees_file = 'assets/forest_management_dataset-trees.csv'
        paths_file = 'assets/forest_management_dataset-paths.csv'

        load_dataset(self.forest, trees_file, paths_file)
        #mock_load_dataset.assert_called_once_with(self.forest, trees_file, paths_file)
        

    @patch.object(Draw, 'draw')
    def test_draw(self, mock_draw):
        # Test drawing the forest
        Draw.draw(self.forest)
        mock_draw.assert_called_once_with(self.forest)
    


    @patch("builtins.print")
    @patch("Forest_Management_System.utils.load_dataset")
    @patch.object(Draw, 'draw')
    @patch("builtins.open", new_callable=mock_open, read_data="sample tree data")
    def test_main_script(self, mock_file, mock_draw, mock_load_dataset, mock_print):
        # Simulate the main script and test the expected output
        trees_file = 'assets/forest_management_dataset-trees.csv'
        paths_file = 'assets/forest_management_dataset-paths.csv'

        load_dataset(self.forest, trees_file, paths_file)
        
        # Check print output for the forest
        print("================================================")
        print(self.forest)
        print("================================================")
        Draw.draw(self.forest)

        self.assertEqual(mock_print.call_count, 5)
        mock_print.assert_any_call("================================================")
        mock_print.assert_any_call(self.forest)
        mock_print.assert_any_call("================================================")
        #mock_load_dataset.assert_called_once_with(self.forest, trees_file, paths_file)
        mock_draw.assert_called_once_with(self.forest)

if __name__ == '__main__':
    unittest.main()
