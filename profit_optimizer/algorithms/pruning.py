from profit_optimizer.utils import logger, timing_decorator


class Pruning:
    def __init__(self, actions: set, max_budget: float, purchase_limit: int):
        self.actions: list = list(actions)
        self.max_budget: float = max_budget
        self.purchase_limit: int = purchase_limit
        self.max_benefits = 0

    def bound(self, i: int, current_cost: float, current_benefits: float) -> float:
        """
        Calculates an upper bound estimate on the potential benefits of taking actions starting
        at the given index, while considering the current cost and benefits. The bound is a heuristic
        used for optimization that assumes remaining budget is spent in a way to achieve the
        maximum possible benefits.

        :param i: Index of the action from where to start calculating the bound.
        :type i: int
        :param current_cost: The current cost incurred so far.
        :type current_cost: int
        :param current_benefits: The current benefits gained so far.
        :type current_benefits: int
        :return: An upper bound estimate of the potential benefits.
        :rtype: float
        """
        # If current cost already exceeds budget, no more actions can be bought
        # Return 0 as upper bound (dead branch)
        if current_cost >= self.max_budget:
            return 0

        remaining_budget = self.max_budget - current_cost

        bound_value = current_benefits
        remaining_actions = self.actions[i:]

        # Greedily consume remaining budget with remaining actions to calculate upper bound
        # This gives the most optimistic estimate of achievable benefits
        for action in remaining_actions:
            action_cost = action.cost

            for quantity in range(1, self.purchase_limit + 1):
                total_cost = action_cost * quantity
                if total_cost <= remaining_budget:
                    remaining_budget -= total_cost
                    bound_value += action.benefits * quantity
                else:
                    # buy a fraction of an action to define the bound as an optimistic solution
                    # not a realistic one
                    if quantity == 1:
                        fraction = remaining_budget / action_cost
                        bound_value += fraction * action.benefits
                    remaining_budget = 0
                    break

            if remaining_budget <= 0:
                break

        return bound_value

    def knapsack_recursive(self, i: int, current_cost: float, current_benefits: float) -> None:
        """
        Applies a recursive solution to solve the knapsack problem for maximizing benefits
        within budget constraints. The method considers the possible inclusion of an action
        and evaluates all branches to find the optimal solution.

        :param i: The current index of the action being analyzed in the actions list
        :type i: int
        :param current_cost: The accumulated cost incurred so far
        :type current_cost: float
        :param current_benefits: The accumulated benefits achieved so far
        :type current_benefits: float
        :return: None
        """
        # Calculate upper bound for this branch
        bound = self.bound(i, current_cost, current_benefits)
        # Prune if this branch cannot yield better solution than current best
        if bound <= self.max_benefits:
            logger.info(
                f"Prune at index {i} - bound = {bound}, "
                f"Max benefits are already: {self.max_benefits}"
                )
            return

        # end of iteration is reached
        if i == len(self.actions):
            if current_benefits > self.max_benefits:
                self.max_benefits = current_benefits
                logger.info(f"New max benefits found: {current_benefits}")
            return

        # Get current action
        action = self.actions[i]
        action_cost = action.cost

        logger.info(f"Analysing action at index {i} --- {action.__repr__()}")

        # Branch 1: buy the action as many times as allowed in self.purchase_limit
        for quantity in range(1, self.purchase_limit + 1):
            total_cost = action_cost * quantity
            if current_cost + total_cost <= self.max_budget:
                self.knapsack_recursive(
                    i + 1,
                    current_cost + total_cost,
                    current_benefits + action.benefits * quantity
                    )

        # Branch 2: Do not buy action, keep current_cost and current_benefits
        # but increment index to deal with next action
        # it is important to execute branch 2 anyway to explore all possible combinations
        self.knapsack_recursive(i + 1, current_cost, current_benefits)

    @timing_decorator("PRUNING")
    def run(self) -> None:
        """
        Executes the Branch and Bound algorithm with pruning, optimized to maximize
        the benefits while respecting budget constraints.
        """
        # Initial sort to optimize pruning
        # Higher ratio actions are explored first, improving bound calculations
        self.actions.sort(key=lambda a: a.benefits, reverse=True)

        # Initialize and run algorithm
        self.max_benefits = 0
        self.knapsack_recursive(0, 0, 0)

        print("=" * 80)
        logger.info(f"Max Benefits: {self.max_benefits}")
        logger.info(f"Total Cost: {self.max_budget}")
