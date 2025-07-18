from profit_optimizer.utils import logger, timing_decorator


class Greedy:
    def __init__(self, actions: set, max_budget: float, purchase_limit: int):
        self.actions: set = actions
        self.max_budget: float = max_budget
        self.purchase_limit: int = purchase_limit

    def sort_actions_by_benefits(self):
        sorted_actions = sorted(self.actions, key=lambda a: a.benefits)
        sorted_actions.reverse()
        return sorted_actions

    def get_best_actions_wallet(self):
        wallet = []
        sorted_actions = self.sort_actions_by_benefits()

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
