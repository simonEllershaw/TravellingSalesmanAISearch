"sampleSpace object constructed from txt file with name, number of cities and 2x2 matrix of cities relations"

import numpy as np
import re

class sampleSpace:
    def __init__(self, aFname):
        "Create sample space from .txt file"
        parsedFile = self.parseInputFile(aFname)
        #re names help https://www.vipinajayakumar.com/parsing-text-with-python/
        self.name = self.getVariableFromFile(parsedFile[0], r"NAME = (?P<variable>.*)")
        self.numberOfCities = int(self.getVariableFromFile(parsedFile[1], r"SIZE = (?P<variable>\d+)"))
        self.cityMatrix = self.getCityMatrix(parsedFile)
        
    def parseInputFile(self, aFname):
        f = open(aFname, "r")
        parsedFile = []
        for line in f:
            #empty lines and \n removed
            if line.strip():
                stripped = line.rstrip('\n,')
                parsedFile = parsedFile + stripped.split(",")
        f.close()
        return parsedFile

    def getVariableFromFile(self, aParsedString, aRegExpression):
        match = re.search(aRegExpression , aParsedString)
        returnVariable = match.group('variable')
        return returnVariable   
    
    def getCityMatrix(self, aParsedFile):
        cityMatrix = np.zeros(shape=(self.numberOfCities, self.numberOfCities))
        # first 2 indicies are name and number of cities
        startIndex = 2
        colCount = self.numberOfCities - 1
        rowNumber = 0
        while startIndex <= (len(aParsedFile) - 1):
            for loopNumber in range(0, colCount):
                distance = int(self.getVariableFromFile(aParsedFile[startIndex + loopNumber], r"(?P<variable>\d+)"))
                cityMatrix[rowNumber, rowNumber + loopNumber + 1] = distance
            #reset variables to next line
            startIndex += colCount
            rowNumber += 1
            colCount -= 1
        #diagonals are always 0 so do not have to be accounted for
        cityMatrix = cityMatrix + cityMatrix.transpose()
        return cityMatrix
    
if __name__ == "__main__": 
    s = sampleSpace("Input/NEWAISearchfile175.txt")
    print(s.name, s.numberOfCities)
    print(s.cityMatrix)




    

    