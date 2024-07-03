from collections import deque
from Forest_Management_System.logic.Health_status import HealthStatus

class Infect:
    @staticmethod
    def spread_infection(forest):
        print("Simulating one step of the contagion process (BFS):")

        if not hasattr(Infect, 'queue'):
            Infect.queue = deque(tree.tree_id for tree_id, tree in forest.trees.items() if tree.health_status == HealthStatus.INFECTED)
            Infect.visited = set(Infect.queue)
            Infect.spread_round = 0

        if not Infect.queue:
            recheck_queue = deque(tree.tree_id for tree_id, tree in forest.trees.items() if tree.health_status == HealthStatus.INFECTED)
            recheck_found_infection = False

            while recheck_queue:
                current_tree_id = recheck_queue.popleft()
                for path in forest.paths:
                    neighbor_id = None
                    if path.tree1.tree_id == current_tree_id and path.tree2.tree_id not in Infect.visited:
                        neighbor_id = path.tree2.tree_id
                    elif path.tree2.tree_id == current_tree_id and path.tree1.tree_id not in Infect.visited:
                        neighbor_id = path.tree1.tree_id

                    if neighbor_id is not None and forest.trees[neighbor_id].health_status != HealthStatus.INFECTED:
                        Infect.visited.add(neighbor_id)
                        forest.trees[neighbor_id].health_status = HealthStatus.INFECTED
                        Infect.queue.append(neighbor_id)
                        print(f"Infection spreads to Tree ID {neighbor_id} from Tree ID {current_tree_id}.")
                        recheck_found_infection = True
                        return

                if recheck_found_infection:
                    break

            if not recheck_found_infection:
                print("No more infections possible. Simulation complete.")
                return
        
        Infect.spread_round += 1
        print(f"ROUND {Infect.spread_round}:")

        if not Infect.queue:
            print("No more trees in the queue to process.")
            return

        print(f"Current infection queue: {list(Infect.queue)}")

        current_tree_id = Infect.queue.popleft()
        infected_this_round = False

        for path in forest.paths:
            neighbor_id = None
            if path.tree1.tree_id == current_tree_id and path.tree2.tree_id not in Infect.visited:
                neighbor_id = path.tree2.tree_id
            elif path.tree2.tree_id == current_tree_id and path.tree1.tree_id not in Infect.visited:
                neighbor_id = path.tree1.tree_id

            if neighbor_id is not None and forest.trees[neighbor_id].health_status != HealthStatus.INFECTED:
                Infect.visited.add(neighbor_id)
                forest.trees[neighbor_id].health_status = HealthStatus.INFECTED
                Infect.queue.append(neighbor_id)
                print(f"Infection spreads to Tree ID {neighbor_id} from Tree ID {current_tree_id}.")
                infected_this_round = True
                break

        if not infected_this_round:
            print(f"No infection spread from Tree ID {current_tree_id} in this round. Retrying...")

        print("Current forest state:")
        for tree in forest.trees.values():
            print(tree)
