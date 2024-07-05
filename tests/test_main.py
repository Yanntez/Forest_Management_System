import unittest
from unittest.mock import patch, MagicMock
from Forest_Management_System.entity.Forest import Forest
from Forest_Management_System.utils import load_dataset
from Forest_Management_System.logic.Draw import Draw
import main

class TestMain(unittest.TestCase):
    @patch('main.load_dataset')
    @patch('main.Draw.draw')
    def test_main(self, mock_draw, mock_load_dataset):
        # Mock the dataset loading
        mock_load_dataset.return_value = None
        
        # Create a mock forest instance
        mock_forest = MagicMock(spec=Forest)
        
        # Replace the Forest instance in main with the mock
        with patch('main.Forest', return_value=mock_forest):
            main.forest = mock_forest
            main.load_dataset(main.forest, main.trees_file, main.paths_file)
            main.Draw.draw(main.forest)
        
        # Assert load_dataset was called with the correct arguments
        mock_load_dataset.assert_called_with(main.forest, main.trees_file, main.paths_file)
        
        # Assert draw was called with the forest instance
        mock_draw.assert_called_with(main.forest)

if __name__ == '__main__':
    unittest.main()