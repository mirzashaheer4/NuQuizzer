import tkinter as tk
from constants import *
from template import Template
from single import Single
from twoplayer import TwoPlayer

class PlayerInfo:
    def __init__(self, Home, single=True):
        self.root = tk.Tk()
        template = Template(self.root, BG_COLOR_3)
        self.Home = Home
        self.single = single
        
        
        # Main Window
        template.mainWindow()

        # Navigation Bar
        template.navigationBar(Home)
        
        # title
        template.title()
        if single:
            # Single Player Info
            self.singlePlayerInfo()
        else:
            self.TwoPlayerInfo()

        # Team
        template.team()

        # Footer
        template.footer()

        #End
        template.end()

    # Player Info Frames

    def singlePlayerInfo(self):
        info_frame = tk.Frame(self.root, bg=BG_COLOR_3)
        info_frame.pack()

        name_label = tk.Label(info_frame, text="Name", height=12, font=("Arial", 20), fg=FG_COLOR_2, bg=BG_COLOR_3)
        name_label.pack(side=tk.LEFT, padx=20)

        name_entry = tk.Entry(info_frame, width=20,fg=BG_COLOR_3, bg=BG_COLOR_4, highlightcolor=BG_COLOR_3, highlightbackground=BG_COLOR_3)
        name_entry.pack(side=tk.LEFT, padx=20)

        start = tk.Button(info_frame, text="START", command=lambda: self.startSingleMode(name_entry.get()),bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, highlightbackground=BTN_HB_COLOR, cursor="hand2")
        start.pack(side=tk.LEFT)

    def TwoPlayerInfo(self):
        info_frame = tk.Frame(self.root, bg=BG_COLOR_3)
        info_frame.pack()

        player1_frame = tk.Frame(info_frame, bg=BG_COLOR_3)
        player1_frame.pack()

        player1_name_label = tk.Label(player1_frame, text="👤 Player 1", height=5, font=("Arial", 20), fg=FG_COLOR_2, bg=BG_COLOR_3)
        player1_name_label.pack(side=tk.LEFT, padx=20)

        player1_name_entry = tk.Entry(player1_frame, fg=BG_COLOR_3, width=20, bg=BG_COLOR_4, highlightcolor=BG_COLOR_3, highlightbackground=BG_COLOR_3)
        player1_name_entry.pack(side=tk.RIGHT, padx=20)

        player2_frame = tk.Frame(info_frame, bg=BG_COLOR_3)
        player2_frame.pack()

        player2_name_label = tk.Label(player2_frame, text="👤 Player 2", height=5 ,font=("Arial", 20), fg=FG_COLOR_2, bg=BG_COLOR_3)
        player2_name_label.pack(side=tk.LEFT, padx=20)

        player2_name_entry = tk.Entry(player2_frame, width=20,fg=BG_COLOR_3, bg=BG_COLOR_4, highlightcolor=BG_COLOR_3, highlightbackground=BG_COLOR_3)
        player2_name_entry.pack(side=tk.RIGHT, padx=20)

        start = tk.Button(info_frame, text="START", command=lambda: self.startTwoPlayerMode(player1_name_entry.get(), player2_name_entry.get()), bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, highlightbackground=BTN_HB_COLOR,cursor="hand2")
        start.pack(pady=(10, 50))
    
    def startTwoPlayerMode(self, player1_name, player2_name):
        self.root.destroy()
        TwoPlayer(self.Home, player1_name, player2_name, self.single)
        
    def startSingleMode(self, name):
        self.root.destroy()
        Single(self.Home, name)
        
