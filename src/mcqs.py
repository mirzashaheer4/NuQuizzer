import pandas as pd
import random
from onefile import resource_path


class MCQS:
    def __init__(self):
        self.fileName = self.randomMCQFile()
        self.file = self.readFile(self.fileName)

    def getFileName(self):
        return self.fileName
    
    def getRandomMCQ(self):
        '''
            return random -> 
            Difficulty
            Question
            OptionA 
            OptionB 
            OptionC 
            OptionD 
            Answer
        '''
        totalRows = self.getTotalRows()
        randomRow = random.randint(0, (totalRows - 1 ))
        randomMCQ = self.file.iloc[randomRow]

        return randomMCQ
        
    def readFile(self, file):
        csvfile = pd.read_csv(resource_path(f"res/mcqs/{file}.csv"))
        csvfile = csvfile.dropna()
        return csvfile
    
    def getTotalRows(self):
        return self.file.shape[0]
    
    def randomMCQFile(self):
        filesNames = ["Business", "English", "GeneralKnowledge", "History", "Logical", "Pakistan", "Science"]
        totoalFiles = len(filesNames)
        randomNumber = random.randint(0, (totoalFiles-1))
        randomMCQFile = filesNames[randomNumber] 
        return randomMCQFile
