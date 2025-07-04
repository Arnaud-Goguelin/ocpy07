from profit_optimizer.utils import logger


class BrutForce:
    def __init__(self, actions: set):
        self.actions: set = actions
        self.max_budget: float = 500.0

    def sort_actions_by_profitability(self):
        sorted_actions = sorted(self.actions, key=lambda a: a.profitability)
        sorted_actions.reverse()
        return sorted_actions

    def get_best_actions_wallet(self):
        wallet = set()
        sorted_actions = self.sort_actions_by_profitability()

        for action in sorted_actions:
            if action.cost <= self.max_budget:
                wallet.add(action)
                self.max_budget -= action.cost
            else:
                break
        return sorted(wallet, key=lambda action: action.profitability, reverse=True)

    def run(self):
        logger.info("Running Brut Force algorithm")
        best_wallet = self.get_best_actions_wallet()
        print(f"{"=" * 10} Best wallet {"=" * 10}")
        for action in best_wallet:
            logger.info(f"Action: {action.name}, Cost: {action.cost}, Profitability: {action.profitability}")
        print("Number of actions: ", len(best_wallet))
        print("Total cost: ", sum(action.cost for action in best_wallet))
