from profit_optimizer.models import Action
from profit_optimizer.utils import logger, timing_decorator


class Greedy:
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
