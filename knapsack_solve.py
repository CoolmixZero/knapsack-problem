from deap import base, creator, tools, algorithms

import random
import numpy

import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns

from knapsack import KnapsackProblem
from properties import Properties

global knapsack


# fitness calculation
def knapsackValue(individual) -> tuple:
    return knapsack.getValue(individual),


# Genetic Algorithm flow:
def main(val: int, properties: Properties):
    # problem constants:
    # create the knapsack problem instance to be used:
    global knapsack
    knapsack = KnapsackProblem(val)

    # set the random seed:
    random.seed(properties.RANDOM_SEED)

    toolbox = base.Toolbox()

    # create an operator that randomly returns 0 or 1:
    toolbox.register("zeroOrOne", random.randint, 0, 1)

    # define a single objective, maximizing fitness strategy:
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))

    # create the Individual class based on list:
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # create the individual operator to fill up an Individual instance:
    toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, len(knapsack))

    # create the population operator to generate a list of individuals:
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

    toolbox.register("evaluate", knapsackValue)

    # genetic operators:mutFlipBit

    # Tournament selection with tournament size of 3:
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Single-point crossover:
    toolbox.register("mate", tools.cxTwoPoint)

    # Flip-bit mutation:
    # indpb: Independent probability for each attribute to be flipped
    toolbox.register("mutate", tools.mutFlipBit, indpb=1.0 / len(knapsack))

    # < - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - >

    # create initial population (generation 0):
    population = toolbox.populationCreator(n=properties.POPULATION_SIZE)

    # prepare the statistics object:
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", numpy.max)
    stats.register("min", numpy.min)
    stats.register("avg", numpy.mean)

    # define the hall-of-fame object:
    hof = tools.HallOfFame(properties.HALL_OF_FAME_SIZE)

    # perform the Genetic Algorithm flow with hof feature added:
    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=properties.P_CROSSOVER, mutpb=properties.P_MUTATION,
                                              ngen=properties.MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

    # print best solution found:
    best = hof.items[0]
    print("\n-- Best Ever Individual = ", best)
    print("\n-- Best Ever Fitness = ", best.fitness.values[0])

    print("\n-- Knapsack Items:\n")
    knapsack.printItems(best)

    # extract statistics:
    maxFitnessValues, meanFitnessValues, minFitnessValues = logbook.select("max", "avg", "min")

    # plot statistics:
    matplotlib.use('TkAgg')

    sns.set_style("ticks")
    plt.plot(maxFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    plt.plot(minFitnessValues, color='yellow')
    plt.xlabel('Generation')
    plt.ylabel('Max(red) / Min(yellow) / Average Fitness(green)')
    plt.title('Max and Average fitness over Generations')

    plt.show()

