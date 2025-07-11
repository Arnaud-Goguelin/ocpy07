from profit_optimizer.utils import logger


class BruteForce:
    def __init__(self, actions: set, max_budget: float, purchase_limit: int):
        self.actions: set = actions
        self.max_budget: float = max_budget
        self.purchase_limit: int = purchase_limit

    def sort_actions_by_profitability(self):
        sorted_actions = sorted(self.actions, key=lambda a: a.profitability)
        sorted_actions.reverse()
        return sorted_actions

    def get_best_actions_wallet(self):
        wallet = []
        sorted_actions = self.sort_actions_by_profitability()

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

    def run(self):
        logger.info("Running Brut Force algorithm")
        print()
        best_wallet = self.get_best_actions_wallet()
        print(f"{"=" * 10} Best wallet {"=" * 10}")
        for action in best_wallet:
            logger.info(f"Action: {action.name}, Cost: {action.cost}, Profitability: {action.profitability}")
        print()
        print("Number of actions: ", len(best_wallet))
        print("Total cost: ", sum(action.cost for action in best_wallet))
        print("=" * 80)
