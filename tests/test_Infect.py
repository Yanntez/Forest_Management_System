import unittest
from collections import deque
from unittest.mock import Mock
from Forest_Management_System.entity.Health_status import HealthStatus
from Forest_Management_System.logic.Infect import Infect

class Tree:
    def __init__(self, tree_id, health_status):
        self.tree_id = tree_id
        self.health_status = health_status

    def __repr__(self):
        return f"Tree({self.tree_id}, {self.health_status})"

class Path:
    def __init__(self, tree1, tree2):
        self.tree1 = tree1
        self.tree2 = tree2

class Forest:
    def __init__(self, trees, paths):
        self.trees = trees
        self.paths = paths

class TestInfect(unittest.TestCase):

    def setUp(self):
        self.tree1 = Tree(1, HealthStatus.HEALTHY)
        self.tree2 = Tree(2, HealthStatus.HEALTHY)
        self.tree3 = Tree(3, HealthStatus.INFECTED)

        self.path1 = Path(self.tree1, self.tree3)
        self.path2 = Path(self.tree2, self.tree3)

        self.forest = Forest({1: self.tree1, 2: self.tree2, 3: self.tree3}, [self.path1, self.path2])

    def tearDown(self):
        if hasattr(Infect, 'queue'):
            delattr(Infect, 'queue')
        if hasattr(Infect, 'visited'):
            delattr(Infect, 'visited')
        if hasattr(Infect, 'spread_round'):
            delattr(Infect, 'spread_round')

    def test_spread_infection_initialization(self):
        Infect.spread_infection(self.forest)
        

    def test_spread_infection_spreads_to_neighbors(self):
        Infect.spread_infection(self.forest)
        Infect.spread_infection(self.forest)
        self.assertEqual(self.tree1.health_status, HealthStatus.INFECTED)
        self.assertNotEqual(self.tree2.health_status, HealthStatus.INFECTED)

    def test_no_more_infections_possible(self):
        Infect.spread_infection(self.forest)
        Infect.spread_infection(self.forest)
        Infect.spread_infection(self.forest)
        self.assertTrue(Infect.queue)
        self.assertEqual(self.tree1.health_status, HealthStatus.INFECTED)
        self.assertEqual(self.tree2.health_status, HealthStatus.INFECTED)
        self.assertEqual(self.tree3.health_status, HealthStatus.INFECTED)

    def test_no_infection_spread_when_all_infected(self):
        self.tree1.health_status = HealthStatus.INFECTED
        self.tree2.health_status = HealthStatus.INFECTED
        Infect.spread_infection(self.forest)
        self.assertTrue(Infect.queue)
        self.assertEqual(self.tree1.health_status, HealthStatus.INFECTED)
        self.assertEqual(self.tree2.health_status, HealthStatus.INFECTED)
        self.assertEqual(self.tree3.health_status, HealthStatus.INFECTED)

if __name__ == '__main__':
    unittest.main()
