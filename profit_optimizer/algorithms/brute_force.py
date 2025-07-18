from profit_optimizer.utils import logger


class BruteForce:
    def __init__(self, actions: set, max_budget: float, purchase_limit: int):
        self.actions: set = actions
        self.max_budget: float = max_budget
        self.purchase_limit: int = purchase_limit

    def run(self):
        logger.info("Running BRUTE FORCE algorithm")

        # dp = dynamic programming
        dp = [0] * (self.max_budget + 1)

        for action in self.actions:
            cost = action.cost
            profitability = action.profitability

            logger.info(action.__repr__())

            for i in range(self.max_budget, cost - 1, -1):
                old_value = dp[i]
                for j in range(1, self.purchase_limit + 1):

                    if i - j * cost >= 0:

                        dp[i] = max(dp[i], dp[i - j * cost] + profitability * j)
                if dp[i] != old_value:
                    logger.info(f"  dp[{j}] = {old_value} -> {dp[j]}")

        return dp[self.max_budget]
