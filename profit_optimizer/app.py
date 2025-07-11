import argparse

from .algorithms import BruteForce
from .models import Data


class Application:

    def __init__(self):
        self.data = Data()
        self.data.load()

    @staticmethod
    def create_parser():
        parser = argparse.ArgumentParser(
            description="Profit Optimizer - Stock Trading Algorithm Suite"
            )

        # Groupe d'arguments mutuellement exclusifs pour les algorithmes
        algo_group = parser.add_mutually_exclusive_group(required=True)

        algo_group.add_argument(
            '--brute-force',
            action='store_true',
            help='Run the brute force algorithm'
            )

        parser.add_argument(
            '--budget',
            type=float,
            default=500.0,
            help='Maximum budget for investments (default: 500.0)'
            )

        parser.add_argument(
            '--limit',
            type=int,
            default=1,
            help='Purchase limit per action (default: 1)'
            )

        return parser

    def run(self):
        print()
        parser = self.create_parser()
        args = parser.parse_args()

        if args.brute_force:
            brute_force = BruteForce(self.data.actions, args.budget, args.limit)
            brute_force.run()
