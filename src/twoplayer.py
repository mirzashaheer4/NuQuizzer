import tkinter as tk
from constants import *
from template import *
from app import *

class TwoPlayer:
    def __init__(self, Home, player1_name, player2_name, single=False):
         # Root 
        self.root = tk.Tk()
        
        # Template Setup
        self.template = Template(self.root, BG_COLOR_3)

        # App Setup
        self.app = App(self.root, BG_COLOR_3, Home, self.template,player1_name,player2_name, single)

        # Attributes
        self.Home = Home
        
        # Main Window
        self.template.mainWindow()

        # Navigation Bar
        self.template.navigationBar(Home)
        
        # MCQ Thread
        self.app.mcqThreadStart()

        # Overall Timer
        self.app.overallTimer()
    
        # Score
        self.app.score()

        # Progress Bar Frame and Thread
        self.app.progressBarThreadStart()

        #End
        self.template.end()
