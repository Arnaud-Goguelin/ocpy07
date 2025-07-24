from profit_optimizer.utils import timing_decorator
from ..models import Action
from ..utils import SCALE_FACTOR


class Knapsack:
    def __init__(self, actions: list[Action], max_budget: float, purchase_limit: int):
        self.actions: list = actions
        self.max_budget: float = max_budget
        self.purchase_limit: int = purchase_limit

    @timing_decorator("KNAPSACK")
    def run(self):
        """
        Run the optimized knapsack algorithm to calculate the maximum possible profit within the given constraints.

        Implements a dynamic programming solution to the knapsack problem, where each possible budget
        amount is treated as an index in an array (`dp`). This algorithm determines the maximum profitability possible
        given a list of actions, each having an associated cost and benefit.
        The solution considers specific constraints, such as the maximum budget and the purchase limit per action.

        The core logic includes:
        - Converting monetary values to integers by scaling, in order to handle decimals in the budget calculations.
        - Iterating over each action and determining whether purchasing it—given the current budget and quantity—yields
          greater profitability compared to the existing state.
        - Using backward iteration over the budget values to ensure
         no action is counted more than once in a single solution.

        Constraints like `purchase_limit` are applied to ensure that no single action
        is bought more than the allowed number of times, and the solution ensures calculations respect these
        constraints.

        :param max_budget: The total monetary budget available.
        :type max_budget: float
        :param actions: List of all possible actions, where each action has associated cost and benefit values.
        :type actions: list[Action]
        :param purchase_limit: The maximum quantity of an individual action that can be purchased.
        :type purchase_limit: int
        :returns: The maximum profitability that can be achieved under the constraints.
        :rtype: int
        """
        # as we work with €, * SCALE_FACTOR to convert € with decimals into int
        # because budget is used as an index in this algo
        max_budget_scaled = int(self.max_budget * SCALE_FACTOR)

        # dp = dynamic programming
        # initialization: dp[current_budget] represents profitability with a current budget
        # in this list, budget is index, value is profitability,
        # max index is equal to max budget (the last index)
        # as budget is index, and index starts at 0, we want to finish at max_budget_scaled + 1 to reach our real
        # max_budget
        # thus here we initialize a list with n budget (thus n index) from 0 to max budget,
        # for the moment all values are 0 because we didn't buy any action yet
        dp = [0] * (max_budget_scaled + 1)

        for action in self.actions:
            cost = int(action.cost * SCALE_FACTOR)
            benefits = action.benefits

            # reminder range(start, stop, step)
            # start = start value, from where we start
            # stop = end value, where we stop, this value is excluded!
            # step = incrementation

            # thus here stop at cost - 1 just after the action cost (in decreasing order),
            # so we stop iteration when action cost is reached
            # indeed, handle cases after this limit would mean the current budget is lower than cost
            # and we could not buy action

            # we can understand this line like this:
            # for all budgets from max_budget to action.cost, check if buying this action
            # increases profitability

            # iterate in max budget in decreasing order to avoid to
            # count several times the same actions in profitability calculation
            # look at calculation formula on line 69 to understand

            # in decreasing order, value for dp[budget] are not yet changed
            # here is an example in ascending order:
            # let's assume quantity = 1,
            #   when budget = cost (the lowest possible); thus dp[cost] = max(dp[cost], dp[cost - cost] + benefits)
            #   as dp[cost] is not yet defined, we have dp[cost] = max(0, dp[0] + benefits)
            #   and eventually dp[cost] = max(0, 0+benefits) => dp[cost] = benefits
            #
            #   when budget = 2 * cost; thus dp[2cost] = max(dp[2cost], dp[2cost - cost] + benefits)
            #   then dp[2cost] = max(dp[2cost], dp[cost] + benefits)
            #   dp[2cost] = max(dp[2cost], benefits + benefits)
            #   dp[2cost] = max(dp[2cost], 2benefits)
            #   but at this point dp[2cost] is not defined yet thus
            #   dp[2cost] = max(0, 2benefits)
            #   dp[2cost] = 2benefits
            #   here when we calculate dp[2cost], dp[cost] already has a value, that means we consider twice
            #   benefits from action in this solution, which is incorrect, when did bought the action in this case
            #   the first time?
            #   what about the quantity set to 1 ? in this case quantity is 2 which do not respect limit
            #
            #   in decreasing order, let's assume quantity = 1,
            #   dp[2cost] = max(dp[2cost], dp[2cost - cost] + benefits)
            #   dp[2cost] = max(dp[2cost], dp[cost] + benefits)
            #   dp[2cost] = max(dp[2cost], 0 + benefits)
            #   dp[2cost] = max(0, benefits)
            #   dp[2cost] = benefits

            for budget in range(max_budget_scaled, cost - 1, -1):
                # buy as many as possible actions, respecting purchase_limit
                # start at 1 because we cannot buy a fraction of an action
                for quantity in range(1, self.purchase_limit + 1):
                    if budget - quantity * cost >= 0:
                        # here we keep max value (understand max profitability)
                        # between current profitability for current budget
                        # and
                        # new calculated profitability for budget - action.cost (thus when we buy the action)
                        # result is put in dp list at index(=budget) place
                        dp[budget] = max(dp[budget], dp[budget - cost * quantity] + benefits * quantity)

        result = dp[max_budget_scaled]
        print("=" * 80)
        print(f"Max Benefits: {result}")
