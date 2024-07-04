import unittest
from collections import deque
from Forest_Management_System.entity.Health_status import HealthStatus
from Forest_Management_System.logic.Infect import Infect
from Forest_Management_System.entity.Path import Path
from Forest_Management_System.entity.Tree import Tree
from Forest_Management_System.entity.Forest import Forest

class TestInfect(unittest.TestCase):
    def setUp(self):
        # Set up the forest with trees and paths for testing
        self.forest = Forest()
        
        self.tree1 = Tree(1, "Oak", 10, HealthStatus.HEALTHY)
        self.tree2 = Tree(2, "Pine", 15, HealthStatus.INFECTED)
        self.tree3 = Tree(3, "Birch", 8, HealthStatus.HEALTHY)
        self.tree4 = Tree(4, "Maple", 20, HealthStatus.HEALTHY)
        
        self.forest.add_tree(self.tree1)
        self.forest.add_tree(self.tree2)
        self.forest.add_tree(self.tree3)
        self.forest.add_tree(self.tree4)
        
        self.forest.add_path(self.tree1.tree_id, self.tree2.tree_id, 5)
        self.forest.add_path(self.tree2.tree_id, self.tree3.tree_id, 10)
        self.forest.add_path(self.tree3.tree_id, self.tree4.tree_id, 15)

        # Clear any previous state in the Infect class
        if hasattr(Infect, 'queue'):
            delattr(Infect, 'queue')
        if hasattr(Infect, 'visited'):
            delattr(Infect, 'visited')
        if hasattr(Infect, 'spread_round'):
            delattr(Infect, 'spread_round')

    def test_spread_infection_initial_infected(self):
        Infect.spread_infection(self.forest)
        self.assertIn(2, Infect.visited)
        self.assertIn(3, Infect.visited)
        self.assertEqual(self.tree3.health_status, HealthStatus.INFECTED)

    def test_spread_infection_no_more_infections(self):
        # Infect all trees in setup
        self.tree1.health_status = HealthStatus.INFECTED
        self.tree3.health_status = HealthStatus.INFECTED
        self.tree4.health_status = HealthStatus.INFECTED
        Infect.spread_infection(self.forest)
        self.assertEqual(Infect.queue, deque())
        self.assertEqual(len(Infect.visited), 4)
        
    def test_spread_infection_multiple_rounds(self):
        Infect.spread_infection(self.forest)
        self.assertEqual(self.tree3.health_status, HealthStatus.INFECTED)
        
        Infect.spread_infection(self.forest)
        self.assertEqual(self.tree4.health_status, HealthStatus.INFECTED)

    def test_no_more_infections_possible(self):
        # Only one infected tree with no paths
        self.forest = Forest()
        self.tree1 = Tree(1, "Oak", 10, HealthStatus.HEALTHY)
        self.tree2 = Tree(2, "Pine", 15, HealthStatus.INFECTED)
        
        self.forest.add_tree(self.tree1)
        self.forest.add_tree(self.tree2)
        
        Infect.spread_infection(self.forest)
        self.assertEqual(len(Infect.visited), 1)
        self.assertEqual(Infect.spread_round, 0)

if __name__ == "__main__":
    unittest.main()
