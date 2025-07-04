class Action:
    def __init__(self, name: str, cost: float, benefits: float):
        self.name = self._validate_name(name)
        self.cost = self._validate_floats(cost)
        self.benefits = self._validate_floats(benefits)

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
        return f"{self.name}, {self.cost}€, {self.benefits}%"

    # need to make object Action hashable to be used in set()
    # here this means name is used has ID
    def __hash__(self):
        return hash(self.name)

    # remember: criteria in __eq__ must be the same than in __hash__
    def __eq__(self, other):
        return self.name == other.name
