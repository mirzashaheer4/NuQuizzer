import csv
import os
import datetime
import pandas as pd
from onefile import resource_path

class FileHandler:
    def __init__(self):
        pass

    # Functions to store data
    def store_record(self, name, score, date, filename=resource_path("stored/stored.csv")):
        file_exists = os.path.isfile(filename) 
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name", "Score", "Date"])
        # Write the new record
            writer.writerow([name, score, date])
        # Sort and then save
        pd.read_csv(filename).sort_values(by=["Score"], ascending=False).to_csv(filename,index=False)
    
    def twoPlayer_Store_record(self, player1, player2, winner, draw, date, filename=resource_path("stored/stored2.csv")):
        file_exists = os.path.isfile(filename) 
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Player 1", "Player 2", "Winner", "Draw","Date"])
        # Write the new record
            if draw:
                writer.writerow([player1, player2, "-", 1,date])
            else:
                writer.writerow([player1, player2, winner, 0,date])
        # Sort and then save
        pd.read_csv(filename).sort_values(by=["Date"], ascending=False).to_csv(filename,index=False)


    # Functions to read and display data from the CSV file
    def fetchTop3(self):
        try:
            csv_file = pd.read_csv(resource_path("stored/stored.csv"))
            csv_file = csv_file.dropna()
            return csv_file.head(3).values.tolist()
        except:
            return []
    

    def fetchRecent(self):
        try:
            csv_file = pd.read_csv(resource_path("stored/stored2.csv"))
            csv_file = csv_file.dropna()
            return csv_file.head(3).values.tolist()
        except:
            return []
    
    def fetchTopAll(self):
        try:
            csv_file = pd.read_csv(resource_path("stored/stored.csv"))
            csv_file = csv_file.dropna()
            return csv_file.values.tolist()
        except:
            pass
    def fetchRecentAll(self):
        try:
            csv_file = pd.read_csv(resource_path("stored/stored2.csv"))
            csv_file = csv_file.dropna()
            return csv_file.values.tolist()
        except:
            return []

    # Functions to take user input and store it
    def single_user_input(self, name, score):
        name = name
        score = score
        date = datetime.datetime.now()
        date = date.strftime("%d/%b/%Y")
        
        self.store_record(name, int(score), date)


    def twoPlayer_user_input(self, player1, player2, winner, draw):
        date = datetime.datetime.now()
        # date = date.strftime("%d/%b/%Y")

        self.twoPlayer_Store_record(player1, player2, winner, draw, date)
