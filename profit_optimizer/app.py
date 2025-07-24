import argparse

from .algorithms import BruteForce, Greedy, Knapsack, Pruning
from .models import Data
from .utils import DataFilesNames, logger


class Application:

    def __init__(self):
        self.data = None

    @staticmethod
    def create_parser():
        parser = argparse.ArgumentParser(description="Profit Optimizer - Stock Trading Algorithm Suite")

        parser.add_argument(
            "--file",
            "-f",
            type=str,
            default=DataFilesNames.test.value,
            help=f"Name of the data file to load, choose between: "
            f"{", ".join([member.value for member in DataFilesNames])} (without extension, default: test)",
        )

        parser.add_argument(
            "--budget", type=float, default=500.0, help="Maximum budget for investments (default: 500.0)"
        )

        parser.add_argument("--limit", type=int, default=1, help="Purchase limit per action (default: 1)")

        # args groups for algorithms only
        algo_group = parser.add_mutually_exclusive_group(required=True)

        algo_group.add_argument(
            "--greedy",
            action="store_true",
            help="Run the greedy algorithm, return the best " "combination of actions with the best benefits.",
        )

        algo_group.add_argument(
            "--knapsack",
            action="store_true",
            help="Run the knapsack algorithm, "
            "return an approximation of the best "
            "benefits reachable with the budget.",
        )

        algo_group.add_argument(
            "--pruning",
            action="store_true",
            help="Run the branch and bound algorithm with pruning optimization, "
            "return the best combination of actions with the best benefits.",
        )

        algo_group.add_argument(
            "--brute",
            action="store_true",
            help="Run the brute force algorithm (explores all combinations), "
            "return the best combination of actions with the best benefits.",
        )

        return parser

    def run(self):
        print()
        parser = self.create_parser()
        args = parser.parse_args()

        if args.file not in DataFilesNames:
            logger.error(
                f"Invalid data file name '{args.file}'."
                f"\nPlease choose between: {", ".join([member.value for member in DataFilesNames])}."
            )

        self.data = Data(file_name=args.file)
        self.data.load()

        if not self.data.actions:
            print("No actions found in the data file. Exit.")
            return

        if args.greedy:
            greedy = Greedy(self.data.actions, args.budget, args.limit)
            greedy.run()

        if args.knapsack:
            knapsack = Knapsack(self.data.actions, args.budget, args.limit)
            knapsack.run()

        if args.pruning:
            pruning = Pruning(self.data.actions, args.budget, args.limit)
            pruning.run()

        if args.brute:
            brute = BruteForce(self.data.actions, args.budget, args.limit)
            brute.run()
