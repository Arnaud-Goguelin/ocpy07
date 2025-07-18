import argparse

from .algorithms import Greedy, Knapsack, Pruning
from .models import Data


class Application:

    def __init__(self):
        self.data = Data()
        self.data.load()

    @staticmethod
    def create_parser():
        parser = argparse.ArgumentParser(description="Profit Optimizer - Stock Trading Algorithm Suite")

        # Groupe d'arguments mutuellement exclusifs pour les algorithmes
        algo_group = parser.add_mutually_exclusive_group(required=True)

        algo_group.add_argument("--greedy", action="store_true", help="Run the greedy algorithm")

        algo_group.add_argument("--knapsack", action="store_true", help="Run the knapsack algorithm")

        algo_group.add_argument("--pruning", action="store_true", help="Run the knapsack algorithm optimized with "
                                                                       "pruning")

        parser.add_argument(
            "--budget", type=float, default=500.0, help="Maximum budget for investments (default: 500.0)"
        )

        parser.add_argument("--limit", type=int, default=1, help="Purchase limit per action (default: 1)")

        return parser

    def run(self):
        print()
        parser = self.create_parser()
        args = parser.parse_args()

        if args.greedy:
            greedy = Greedy(self.data.actions, args.budget, args.limit)
            greedy.run()

        if args.knapsack:
            knapsack = Knapsack(self.data.actions, args.budget, args.limit)
            knapsack.run()

        if args.pruning:
            pruning = Pruning(self.data.actions, args.budget, args.limit)
            pruning.run()
