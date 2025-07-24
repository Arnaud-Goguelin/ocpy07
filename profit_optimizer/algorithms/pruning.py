from profit_optimizer.models import Action
from profit_optimizer.utils import timing_decorator


class Pruning:

    """
    Branch-and-Bound algorithm with pruning for the knapsack problem.
    Intelligently explores the solution space by eliminating unpromising branches.

    Time Complexity:
        - Worst case: O((L+1)^n) - identical to brute force if no pruning occurs
        - Average case: O(2^(n/2)) to O(2^(3n/4)) - thanks to effective pruning
            note: those are just empirical observations
        - Best case: O(n²) - when pruning is highly effective
        where n = number of actions, L = purchase_limit

        Efficiency depends on:
        - Quality of the bound() function (upper bound)
        - Initial sorting order of actions (by decreasing benefits is the best in our case)
        - Diversity of action costs/benefits (the bigger the gaps the better)

    Space Complexity: O(n) where:
        - n = number of actions (maximum recursion depth)
        - Additional O(k) for storing the best combination, where k ≤ n*L
        - The current_combination list grows and shrinks during backtracking
        - Overall space is dominated by recursion stack: O(n)
        - Space identical to brute force despite temporal optimization

    Pruning advantages:
        - Eliminates unpromising branches through bound()
        - Initial sorting optimizes exploration order
        - Quickly finds good solutions to improve pruning effectiveness

    Note: DO NOT guarantee the optimal solution like brute force,
    unless we have an initial sorting of actions by decreasing benefits.
    But it is much more efficient.
    """

    def __init__(self, actions: set[Action], max_budget: float, purchase_limit: int):
        self.actions: list = list(actions)
        self.max_budget: float = max_budget
        self.purchase_limit: int = purchase_limit
        self.max_benefits = 0
        self.best_cost = 0
        self.best_combination = []
        self.branch_explored = 0
        self.branch_pruned = 0

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

    def branch_and_bound_recursive(
        self,
        i: int,
        current_cost: float,
        current_benefits: float,
        current_combination: list[Action],
    ) -> None:
        """
        Performs the branch-and-bound recursive search algorithm to determine the
        optimal combination of actions within a given budget. The method explores
        all possible combinations of actions, calculating and pruning branches
        that cannot provide improved results based on a computed upper bound.

        :param i: Index of the current action being processed in the actions list
        :type i: int
        :param current_cost: The cumulative cost of the actions in the current combination
        :type current_cost: float
        :param current_benefits: The cumulative benefits of the actions in the current combination
        :type current_benefits: float
        :param current_combination: The ongoing combination of actions being constructed in the current branch
        :type current_combination: list[Action]
        :return: None, as the method modifies instance attributes directly during execution
        :rtype: None
        """
        self.branch_explored += 1
        # Calculate upper bound for this branch
        bound = self.bound(i, current_cost, current_benefits)
        # Prune if this branch cannot yield better solution than current best
        if bound <= self.max_benefits:
            self.branch_pruned += 1
            return

        # end of iteration is reached
        if i == len(self.actions):
            if current_benefits > self.max_benefits:
                self.max_benefits = current_benefits
                self.best_cost = current_cost
                self.best_combination = current_combination.copy()

            return

        # Get current action
        action = self.actions[i]
        action_cost = action.cost

        # Branch 1: buy the action as many times as allowed in self.purchase_limit
        for quantity in range(1, self.purchase_limit + 1):
            total_cost = action_cost * quantity
            if current_cost + total_cost <= self.max_budget:
                for _ in range(quantity):
                    current_combination.append(action)

                self.branch_and_bound_recursive(
                    i + 1,
                    current_cost + total_cost,
                    current_benefits + action.benefits * quantity,
                    current_combination,
                )

                # Backtrack: once branch is explored,
                # remove last action added to explore other branches
                for _ in range(quantity):
                    current_combination.pop()

        # Branch 2: Do not buy action, keep current_cost and current_benefits
        # but increment index to deal with next action
        # it is important to execute branch 2 anyway to explore all possible combinations
        self.branch_and_bound_recursive(i + 1, current_cost, current_benefits, current_combination)

    @timing_decorator("PRUNING")
    def run(self) -> None:
        """
        Executes the Branch and Bound algorithm with pruning, optimized to maximize
        the benefits while respecting budget constraints.
        """
        # Initial sort to optimize pruning
        # Higher ratio actions are explored first, improving bound calculations
        # MOREOVER: use a list is necessary with this algorithm to get each time the same result
        # if we keep a set, it is not ordered, and pruning algo may reach different bounds each time and not find
        # the same result each time
        self.actions.sort(key=lambda a: a.benefits, reverse=True)

        # Initialize and run algorithm
        self.max_benefits = 0
        self.branch_and_bound_recursive(0, 0, 0, [])

        print("=" * 80)
        print(f"{"=" * 10} Best wallet {"=" * 10}")
        self.best_combination.sort(key=lambda a: a.benefits, reverse=True)
        for action in self.best_combination:
            print(f"Action: {action.name}, Cost: {action.cost}, Benefits: {action.benefits}")
        print()
        print(f"Max Benefits: {self.max_benefits}")
        print(f"Total Cost: {self.best_cost}")
        print(f"Branch explored: {self.branch_explored}")
        print(f"Branch pruned: {self.branch_pruned}")
