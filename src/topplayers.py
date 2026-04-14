import tkinter as tk
from constants import *
from template import Template

class TopPlayers:
    def __init__(self, Home):
        self.root = tk.Tk()
        template = Template(self.root, BG_COLOR_3)
        self.Home = Home
        
        
        # Main Window
        template.mainWindow()

        # Navigation Bar
        template.navigationBar(Home)
        
        # title
        template.title()

        # Players Window
        self.playersWindow()

        # Team
        template.team()

        # Footer
        template.footer()

        #End
        template.end()


    def playersWindow(self):
        mainFrame = tk.Frame(self.root, bg=BG_COLOR_4, width=400)
        mainFrame.pack()

        # Sub Frames
        nameFrame = tk.Frame(mainFrame, bg=BG_COLOR_4)
        nameFrame.pack(side=tk.LEFT)

        scoreFrame = tk.Frame(mainFrame,bg=BG_COLOR_4)
        scoreFrame.pack(side=tk.RIGHT)

        dateFrame = tk.Frame(mainFrame,bg=BG_COLOR_4)
        dateFrame.pack(side=tk.RIGHT)

        # Headings
        nameLabel = tk.Label(nameFrame, text="Name", anchor="e", bg=BG_COLOR_4, fg=BG_COLOR_3, font=("Arial", 20, "bold"))
        nameLabel.pack()

        scoreLabel = tk.Label(scoreFrame, text="Score", anchor="e", bg=BG_COLOR_4, fg=BG_COLOR_3, font=("Arial", 20, "bold"))
        scoreLabel.pack()

        dateFrame = tk.Label(dateFrame, text="Date", anchor="e", bg=BG_COLOR_4, fg=BG_COLOR_3, font=("Arial", 20, "bold"))
        dateFrame.pack()


    
