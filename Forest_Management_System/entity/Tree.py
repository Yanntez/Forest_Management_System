from ..logic.Health_status import HealthStatus

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
