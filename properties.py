from dataclasses import dataclass


@dataclass()
class Properties:
    # Genetic Algorithm constants:
    POPULATION_SIZE: int = 100
    P_CROSSOVER: float = 0.9  # probability for crossover
    P_MUTATION: float = 0.1  # probability for mutating an individual
    MAX_GENERATIONS: int = 50
    HALL_OF_FAME_SIZE: int = 1
    RANDOM_SEED: int = 42
