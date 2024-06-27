import unittest
from Forest_Management_System.logic.Health_status import HealthStatus
from Forest_Management_System.entity.Tree import Tree  

class TestTree(unittest.TestCase):
    def setUp(self):
        # Create Tree objects for testing
        self.tree1 = Tree(tree_id=1, species="Oak", age=50, health_status=HealthStatus.HEALTHY)
        self.tree2 = Tree(tree_id=2, species="Pine", age=30, health_status=HealthStatus.INFECTED)
        self.tree3 = Tree(tree_id=3, species="Birch", age=20, health_status=HealthStatus.AT_RISK)
        self.tree_invalid_health_status = Tree(tree_id=4, species="Maple", age=15, health_status="Not a HealthStatus object")

    def test_initialization(self):
        self.assertEqual(self.tree1.tree_id, 1)
        self.assertEqual(self.tree1.species, "Oak")
        self.assertEqual(self.tree1.age, 50)
        self.assertEqual(self.tree1.health_status, HealthStatus.HEALTHY)

    def test_health_status_type(self):
        # Test with valid HealthStatus object
        self.assertIsInstance(self.tree1.health_status, HealthStatus)

        # Test with invalid health_status
        self.assertIsNone(self.tree_invalid_health_status.health_status)

    def test_repr(self):
        self.assertEqual(repr(self.tree1), "Tree(ID: 1, Species: Oak, Age: 50, Health Status: HEALTHY)")
        self.assertEqual(repr(self.tree2), "Tree(ID: 2, Species: Pine, Age: 30, Health Status: INFECTED)")

    def test_equality(self):
        tree1_duplicate = Tree(tree_id=1, species="Oak", age=60, health_status=HealthStatus.INFECTED)
        self.assertEqual(self.tree1, tree1_duplicate)
        self.assertNotEqual(self.tree1, self.tree2)

    def test_less_than(self):
        self.assertTrue(self.tree3 < self.tree1)
        self.assertTrue(self.tree3 < self.tree2)
        self.assertFalse(self.tree1 < self.tree2)
        self.assertFalse(self.tree1 < self.tree3)

if __name__ == '__main__':
    unittest.main()
