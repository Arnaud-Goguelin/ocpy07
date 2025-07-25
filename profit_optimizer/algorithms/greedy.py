from profit_optimizer.models import Action
from profit_optimizer.utils import logger, timing_decorator


class Greedy:
    """
    Greedy algorithm for the knapsack problem.
    Selects actions in order of decreasing benefits until budget is exhausted.

    Time Complexity: O(n * log n) where:
        - O(n log n) for sorting actions by benefits (dominant operation)
        - O(n * L) for the greedy selection loop
        - Overall: O(n log n) since sorting dominates when L is small
        where n = number of actions, L = purchase_limit

    Space Complexity: O(n) where:
        - O(n) for the sorted_actions list (copy of original actions)
        - O(k) for the wallet list, where k ≤ n*L (selected actions)
        - No recursion, so no stack overhead
        - Linear space usage, very memory efficient

    Note: This is a heuristic (understand by :quick and simple) algorithm that provides a good approximation
    quickly, but doesn't guarantee the globally optimal solution.
    """

    def __init__(self, actions: set[Action], max_budget: float, purchase_limit: int):
        self.actions: list = list(actions)
        self.max_budget: float = max_budget
        self.purchase_limit: int = purchase_limit

    def get_best_actions_wallet(self):
        """
        Selects the best actions for a wallet based on the sorted by benefits actions list
        while adhering to the constraints of the maximum budget and purchase limit. The selected
        actions are greedily added to the wallet until no more actions can be purchased within
        the budget or the purchase limit is exhausted.

        :return: A list of selected actions ordered by their benefits
        :rtype: list
        """
        wallet = []
        sorted_actions = sorted(self.actions, key=lambda a: a.benefits, reverse=True)

        for action in sorted_actions:
            purchase_count = 0
            while purchase_count < self.purchase_limit:
                if action.cost <= self.max_budget:
                    wallet.append(action)
                    self.max_budget -= action.cost
                    purchase_count += 1
                else:
                    break
        return wallet

    @timing_decorator("GREEDY")
    def run(self):
        best_wallet = self.get_best_actions_wallet()
        print()
        print(f"{"=" * 10} Best wallet {"=" * 10}")
        for action in best_wallet:
            logger.info(f"Action: {action.name}, Cost: {action.cost}, Benefits: {action.benefits}")
        print()
        print("Number of actions: ", len(best_wallet))
        print("Total cost: ", sum(action.cost for action in best_wallet))
        print("Total benefits: ", sum(action.benefits for action in best_wallet))
        print(
            "Profitability: ",
            (sum(action.benefits for action in best_wallet) / sum(action.cost for action in best_wallet)) * 100,
            "%",
        )
