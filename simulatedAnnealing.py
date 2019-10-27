####################################################################

# Implements list dependent simulated annealing (LDSA) algorithm as
# as proposed by Zhan et al

# Author : Simon Ellershaw

#####################################################################

import numpy as np
import random
import utility
import os


def LDSA(fname, p0=0.1, length=150):
    """Main function returns best found state"""
    # initiate TSP variables
    TSP = utility.TSP(fname)
    x = utility.state(TSP)  # create random state
    tempList = createInitialTempList(p0, TSP, length)
    bestState = x

    # set initial loop variables
    numContStates = 0
    mlength = max(TSP.numberOfCities * 2, 800)
    temp = 5  # gets loop started
    i = 0

    while temp > 2 and numContStates < 10:  # outer loop
        temp = tempList[0]
        tMem = []
        numContStates += 1
        i += 1  # count at print number of outer loops
        print(i)

        for m in range(mlength):  # inner loop
            y = greedyHybridNeighbour(x, TSP)

            # Metropolis algorithm
            deltaE = y.length - x.length
            if deltaE <= 0:
                x = y
                if x.length < bestState.length:  # check if new best state
                    bestState = x
                    numContStates = 0  # reset number of cont states
            else:
                r = random.random()
                if r < np.exp(-deltaE / temp):
                    x = y
                    t = -deltaE / np.log(r)
                    tMem.append(t)

        # if new t recorded tempList is updated in Markov loop
        if len(tMem) > 0:
            tempList.pop(0)
            avT = sum(tMem) / len(tMem)
            tempList.append(avT)
            tempList.sort(reverse=True)

    return bestState


def createInitialTempList(p0, aTSP, length):
    """Creates and returns initial temp list"""
    x = utility.state(aTSP)  # random state
    tempList=[]
    for i in range(length):
        y = greedyHybridNeighbour(x, aTSP)  # get neighbour
        if y.length < x.length:
            x = y
        t = -abs(y.length-x.length)/np.log(p0)  # LDSA formula
        tempList.append(t)
    tempList.sort(reverse=True)  # order high to low
    return tempList


def greedyHybridNeighbour(aState, aTSP):
    """Implementation of greedy hybrid neighbourhood structure"""
    x = aState.tour[:]
    del x[len(x) - 1]  # delete last index to stop circularity

    swapIndex = random.sample(range(1, len(x) - 1), 2)  # choose two random ordered indices
    swapIndex.sort()

    # get 3 neighbouring tours by 3 operators and choose smallest tour
    neighbourTours = [inverse(x[:], swapIndex), insert(x[:], swapIndex), swap(x[:], swapIndex)]
    minTourLength = np.inf
    y = []
    for tour in neighbourTours:
        if utility.getTourLength(tour, aTSP) < minTourLength:
            y = tour
            minTourLength = utility.getTourLength(tour, aTSP)

    y.append(y[0])  # make neighbour tour circular
    return utility.state(aTSP, y)


def inverse(aTour, swapIndex):
    """Inverse operator"""
    aTour[swapIndex[0]:swapIndex[1] + 1] = reversed(aTour[swapIndex[0]:swapIndex[1] + 1])
    return aTour

def insert(aTour, swapIndex):
    """Insert operator"""
    insertElement = aTour.pop(swapIndex[1])
    aTour.insert(swapIndex[0], insertElement)
    return aTour

def swap(aTour, swapIndex):
    """Swap operator"""
    aTour[swapIndex[0]], aTour[swapIndex[1]] = aTour[swapIndex[1]], aTour[swapIndex[0]]
    return aTour

if __name__ == "__main__":
    for filename in os.listdir("cityfiles"):
        fname = "cityfiles/" + filename
        bestState = LDSA(fname)
        bestState.saveToFile("Results/TourfileA")
