from profit_optimizer.models import Action
from profit_optimizer.utils import timing_decorator


class BruteForce:

    """
    Brute Force algorithm for the knapsack problem that explores all possible combinations
    of actions to find the optimal solution.

    Time Complexity: O((L+1)^n) where:
        - n = number of actions
        - L = purchase_limit
        - For each action, we have (L+1) choices: buy 0, 1, 2, ..., L quantities
        - This results in (L+1)^n total combinations to explore
        - When L=1 (typical case), this simplifies to O(2^n),
        2 is the number of choices we have for each action: buy it or not

    Space Complexity: O(n) where:
        - n = number of actions (maximum recursion depth)
        - Additional O(k) for storing the best combination, where k ≤ n*L (because of contraint: the budget)
        - The current_combination list grows and shrinks during backtracking
        - Overall space is dominated by recursion stack: O(n)

    Note: This algorithm guarantees finding the optimal solution but becomes
    impractical for large datasets due to exponential time complexity.
    """


    def __init__(self, actions: set[Action], max_budget: float, purchase_limit: int):
        self.actions: list = list(actions)
        self.max_budget: float = max_budget
        self.purchase_limit: int = purchase_limit
        self.best_combination = []
        self.best_benefits = 0.0
        self.best_cost = 0.0
        self.combinations_explored = 0

    def _generate_branch_recursive(
        self,
        index: int,
        current_actions_combination: list[Action],
        remaining_budget: float,
    ):
        """
        Recursively generates action combinations to maximize benefits within
        a given budget and constraints. Explores all potential branches by either
        including or excluding an action in the current combination. Updates
        the best combination found if it results in higher benefits and
        remains within budget.

        :param index: Integer representing the current index of the action
            being explored in the actions list.
        :type index: int
        :param current_actions_combination: List of Action objects currently
            being considered in this branch.
        :type current_actions_combination: list[Action]
        :param remaining_budget: Float value representing the remaining budget
            available for exploring further branches.
        :type remaining_budget: float
        :return: None. The function operates recursively, updating the instance's
            best combination, cost, and benefits as needed.
        :rtype: None
        """

        self.combinations_explored += 1

        # in case we reach last action
        if index == len(self.actions):

            total_cost = sum(action.cost for action in current_actions_combination)
            total_benefits = sum(action.benefits for action in current_actions_combination)

            # check if it generate better benefits and keep it in memory
            if total_benefits > self.best_benefits and total_cost <= self.max_budget:
                self.best_benefits = total_benefits
                self.best_cost = total_cost
                self.best_combination = current_actions_combination.copy()
            # end function here
            return

        # if we did not reach last action, we have 2 choices to generate the branch
        # first choice: do not purchase action and continue to explore the branch
        # by calling recursively _generate_branch_recursive
        self._generate_branch_recursive(index + 1, current_actions_combination, remaining_budget)

        # seconde choice: buy the action and continue exploring this new branch by calling recursively
        # _generate_branch_recursive
        current_action = self.actions[index]

        if current_action.cost <= self.max_budget:
            for quantity in range(1, self.purchase_limit + 1):
                total_cost = current_action.cost * quantity
                if total_cost <= remaining_budget:
                    current_actions_combination.append(current_action)

                    self._generate_branch_recursive(
                        index + 1, current_actions_combination, remaining_budget - total_cost
                    )

                    # Backtrack: once branch is explored,
                    # remove last action added to explore other branches
                    current_actions_combination.pop()

    @timing_decorator("BRUTE FORCE")
    def run(self) -> None:
        # Initialize and run algorithm
        self.best_benefits = 0
        self._generate_branch_recursive(0, [], self.max_budget)

        print("=" * 80)
        print(f"{"=" * 10} Best wallet {"=" * 10}")
        self.best_combination.sort(key=lambda a: a.benefits, reverse=True)
        for action in self.best_combination:
            print(f"Action: {action.name}, Cost: {action.cost}, Benefits: {action.benefits}")
        print()
        print(f"Combinations explored: {self.combinations_explored}")
        print(f"Best Benefits: {self.best_benefits}")
        print(f"Total Cost: {self.best_cost}")
