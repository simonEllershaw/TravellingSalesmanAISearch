####################################################################

# Implementation of a genetic algorithm for TSP

# Author : Simon Ellershaw

#####################################################################

import utility
import numpy as np
import random
import os


def geneticAlgorithm(fname, popSize=200, mutateProb=0.1):
    """Main function returns best found state"""
    sampleSpace = utility.TSP(fname)

    # create a random ordered starting population
    population = []
    for i in range(popSize):
        population.append(utility.state(sampleSpace))
    population.sort(key=lambda state: state.length)  # population in order of state lengths

    #  loop variables
    consecAnswers = 0
    numIteration = 0
    best_allTime = population[0]

    while consecAnswers < 10000:
        cumulativeProbs = getCumulativeProbabilities(population)

        # create child
        father, mother = selectParents(population, cumulativeProbs)
        childTour = ox1(father, mother)  # crossover operator
        if random.random() < mutateProb:
            childTour = ivm(childTour[:])  # mutator operator

        # child replaces worst in population if it has a shorter length
        if utility.getTourLength(childTour, sampleSpace) < population[-1].length:
            child = utility.state(sampleSpace, aTour=childTour)
            population[-1] = child
            population.sort(key=lambda state: state.length)  # reorder population

        # check if best of generation is best of all time if so update
        best_generation = population[0]
        if best_generation.length < best_allTime.length:
            best_allTime = best_generation
            consecAnswers = 0  # reset
        else:
            consecAnswers += 1

        # count and print number of iterations
        numIteration += 1
        print(numIteration)

    return best_allTime


def getCumulativeProbabilities(population):
    """Create list of cumulative probabilities inversely proportional to state length"""
    relLengths = np.zeros(len(population))
    for i in range(len(population)):  # last state in population is the worst
        relLengths[i] = population[-1].length - population[i].length + 1  # add one in case all states the same length
    totalStateLengths = sum(relLengths) + 1
    probBins = (relLengths) / totalStateLengths

    cumulativeProbs = [sum(probBins[:i + 1]) for i in range(len(probBins))]
    cumulativeProbs[-1] = 1  # rounding errors means not always equal to 0
    return cumulativeProbs


def selectParents(aPopulation, cumulativeProbs):
    """Return two members of population with bias towards states with short length"""
    parents = []
    for n in range(2):
        r = random.random()
        parentFound = False
        i = 0
        while not(parentFound):  # iterate across probabilities till r is less than current value
            i += 1
            if r <= cumulativeProbs[i]:
                parents.append(aPopulation[i])
                parentFound = True
    return parents


def ivm(tour):
    """Mutator operator: randomly splice sub tour, reverse and reinsert"""
    del tour[-1]  # get rid of circular nature
    spliceSites = random.sample(range(1, len(tour) - 1), 2)
    spliceSites.sort()

    splice = []
    for i in range(spliceSites[1], spliceSites[0], -1):  # reverse order so don't pop an index no longer there
        splice.append(tour.pop(i))

    insertIndex = random.randint(0, len(tour) - 1)  # already reversed so just randomly reinsert
    tour[insertIndex:insertIndex] = splice
    tour.append(tour[0])  # make circular again
    return tour


def ox1(father, mother):
    """Implementation of order crossover operator"""
    numCities = len(father.tour) - 1  # end city not included in cross as circular

    # get 2 random different ordered splice points
    splice = random.sample(range(1, numCities), 2)
    splice.sort()

    childTour = [-1] * numCities  # -1 never appears in state
    childTour[splice[0]: splice[1]] = father.tour[splice[0]: splice[1]]  # splice from father
    currentMotherIndex = splice[1]  # start at RHS splice site
    childIndex = splice[1]
    while not (childIndex == splice[0]):  # crossover complete when original LHS splice site is found
        if mother.tour[currentMotherIndex] not in childTour:
                childTour[childIndex] = mother.tour[currentMotherIndex]
                if childIndex == numCities - 1:  # move from max index to index 0
                    childIndex = 0
                else:
                    childIndex += 1  # childIndex only increased when city added
        currentMotherIndex += 1  # always move through mother even if not added
        if currentMotherIndex == numCities:
            currentMotherIndex = 0

    childTour.append(childTour[0])  # makes tour circular
    return childTour


if __name__ == "__main__":
    for filename in os.listdir("cityfiles"):
        fname = "cityfiles/" + filename
        bestState = geneticAlgorithm(fname)
        bestState.saveToFile("Results/tourfileB")
