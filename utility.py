####################################################################

# Utility functions and objects to represent TSP and states. Used
# in simAnnealing and geneticAlgorithm

# Author : Simon Ellershaw

#####################################################################

import random
import numpy as np
import re


class TSP:
    def __init__(self, aFname):
        """Create an object representation of the input TSP file"""
        parsedFile = self.parseInputFile(aFname)
        self.name = self.getVariableFromFile(parsedFile[0], r"NAME = (?P<variable>.*)")
        self.numberOfCities = int(self.getVariableFromFile(parsedFile[1], r"SIZE = (?P<variable>\d+)"))
        self.cityMatrix = self.setCityMatrix(parsedFile)

    def parseInputFile(self, aFname):
        """Parse input file into usable string list"""
        f = open(aFname, "r")
        parsedFile = []
        for line in f:
            # empty lines and \n removed
            if line.strip():
                stripped = line.rstrip('\n,')
                parsedFile = parsedFile + stripped.split(",")
        f.close()
        return parsedFile

    def getVariableFromFile(self, aParsedString, aRegExpression):
        """Search and return variable from parsed file"""
        match = re.search(aRegExpression, aParsedString)
        returnVariable = match.group('variable')
        return returnVariable

    def setCityMatrix(self, aParsedFile):
        """Create nxn symetric matrix with coordinates the cities and the value the distance between them"""
        # initialise variables
        cityMatrix = np.zeros(shape=(self.numberOfCities, self.numberOfCities))
        currentIndex = 2   # first 2 indices skipped as are name and number of cities
        colCount = self.numberOfCities - 1
        rowNumber = 0

        while currentIndex <= (len(aParsedFile) - 1):
            for loopNumber in range(0, colCount):
                # get distance from file and place in correct cell
                distance = int(self.getVariableFromFile(aParsedFile[currentIndex + loopNumber], r"(?P<variable>\d+)"))
                cityMatrix[rowNumber, rowNumber + loopNumber + 1] = distance

            # reset variables to next line
            currentIndex += colCount
            rowNumber += 1
            colCount -= 1

        # symmetric matrix so can be transposed as diagonals are 0
        cityMatrix = cityMatrix + cityMatrix.transpose()
        return cityMatrix


class state:
    def __init__(self, aTSP, aTour = []):
        """Object rep of a state can be created from a given or a random tour city numbers
        are one less than in input files so they match with cityMatrix indices"""
        if not aTour:  # if no tour given a valid random circular tour is created
            cities = list(range(aTSP.numberOfCities))
            tour = []
            while len(cities) > 0:  # move a random index city to tour list until no cities remain
                randCityIndex = random.randint(0, len(cities) - 1)
                tour.append(cities.pop(randCityIndex))
            tour.append(tour[0])  # Makes tour circular
        else:
            tour = aTour

        #  set properties
        self.tour = tour
        self.TSP = aTSP
        self.length = getTourLength(self.tour, self.TSP)

    def saveToFile(self, directory):
        """Saves state to file in the given format"""
        saveName = directory + "/tourNEW" + self.TSP.name + ".txt"
        file = open(saveName, "w+")
        file.write("NAME = %s,\r\n" % self.TSP.name)
        file.write("TOURSIZE = %d,\r\n" % self.TSP.numberOfCities)
        file.write("LENGTH = %d,\r\n" % self.length)
        saveState = [x+1 for x in self.tour[1:]]  # get rid of circular part and add 1 to all cities to be in correct format
        file.write(','.join(map(repr, saveState)))


    def tourIsValid(self, aTour):
        """Check that tour is valid"""
        unique = []
        if not (aTour[0] == aTour[len(aTour) - 1]):  # check circular
            return False
        for city in aTour[1:]:  # check each city only in tour once
            if city in unique:
                return False
            else:
                unique.append(city)
        return True

def getTourLength(aTour, aTSP):
    """Returns length of a given tour"""
    tourLength = 0
    # iterate through tour getting relative distances from city matrix
    for i in range(len(aTour) - 1): # don't do final circular index
        tourLength += aTSP.cityMatrix[aTour[i], aTour[i+1]]
    return tourLength
