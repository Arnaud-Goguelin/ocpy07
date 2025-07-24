class Action:
    def __init__(self, name: str, cost: float, profitability: float):
        self.name = self._validate_name(name)
        self.cost = self._validate_floats(cost)
        self.profitability = self._validate_floats(profitability)

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        elif len(name) == 0:
            raise ValueError("name must not be empty")
        return name

    @staticmethod
    def _validate_floats(arg: float) -> float:
        if isinstance(arg, str):
            if not arg.isdigit():
                raise TypeError(f"{arg} must be a float")
            arg = float(arg)

        if arg < 0:
            raise ValueError(f"{arg} must be positive")

        return arg

    def __repr__(self):
        return f"{self.name}, benefits = {self.benefits}"

    # Identify same objects can make algorithms faster, avoiding analyzing duplicates
    def __eq__(self, other):
        return self.benefits == other.benefits and self.cost == other.cost

    # remember: criteria in __eq__ must be the same than in __hash__
    def __hash__(self):
        return hash((self.benefits, self.cost))

    @property
    def benefits(self):
        return (self.profitability / 100) * self.cost
