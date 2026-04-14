import tkinter as tk
from tkinter import messagebox
from constants import *
from template import Template
from app import App

class Single:
    def __init__(self, Home, name,single=True):
        # Root 
        self.root = tk.Tk()
        
        # Template Setup
        self.template = Template(self.root, BG_COLOR_3)

        # App Setup
        self.app = App(self.root, BG_COLOR_3, Home, self.template,name, single)

        # Attributes
        self.Home = Home
        self.name = name
        
        
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

    
    
