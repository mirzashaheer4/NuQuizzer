import tkinter as tk
from constants import *
from template import Template
from playerInfo import PlayerInfo
from filehandler import FileHandler
from recentwins import RecentWins

class Home:
    def __init__(self):
        self.root = tk.Tk()
        template = Template(self.root, BG_COLOR_3)
        self.csvhandler = FileHandler()

        # Main Window
        template.mainWindow()

        # Navigation Bar
        template.navigationBar(Home)

        # Title
        template.title()

        # Score Board (Top Players)
        self.scoreBoard()

        #Main Buttons
        self.buttons()

        # Team
        template.team()        

        # Footer Label
        template.footer()
        template.end()

    #Frames Functions
        
    def buttons(self):
        # Button Frame
        button_frame = tk.Frame(self.root, bg=BG_COLOR_3)
        button_frame.pack(pady=20)

        # Buttons
        single_player_btn = tk.Button(button_frame, command=lambda: self.singlePlayer(Home), text="1 Player Mode",font=("Arial", 14), bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, highlightbackground=BTN_HB_COLOR, width=15, height=2, borderwidth=0, cursor="hand2")
        single_player_btn.pack(pady=10, padx=20, side=tk.LEFT)

        double_player_btn = tk.Button(button_frame,command=lambda: self.twoPlayer(Home), text="2 Player Mode",font=("Arial", 14), bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, highlightbackground=BTN_HB_COLOR, width=15, height=2, borderwidth=0, cursor="hand2")
        double_player_btn.pack(pady=10, padx=20, side=tk.LEFT)
            
    #ScoreBoard
    def scoreBoard(self):
        top3lists = self.csvhandler.fetchTop3()
        recentLists = self.csvhandler.fetchRecent()

        mainFrame = tk.Frame(self.root, bg=BG_COLOR_3)
        mainFrame.pack(fill=tk.BOTH)

        top_players_frame = tk.Frame(mainFrame, bg=BG_COLOR_3)
        top_players_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        top_players_label = tk.Label(top_players_frame, text="Top Players 🏅", font=("Arial", 20, "bold"),bg=BG_COLOR_3, fg=FG_COLOR_2)
        top_players_label.pack(pady=20)

        listbox = tk.Frame(top_players_frame, bg=BG_COLOR_3)
        listbox.pack()

        itemFrames = []

        itemFrame1 = tk.Frame(listbox, bg=BG_COLOR_3)
        itemFrame1.pack(fill=tk.BOTH)

        itemFrame2 = tk.Frame(listbox, bg=BG_COLOR_3)
        itemFrame2.pack(fill=tk.BOTH)

        itemFrame3 = tk.Frame(listbox, bg=BG_COLOR_3)
        itemFrame3.pack(fill=tk.BOTH)

        itemFrames.append(itemFrame1)
        itemFrames.append(itemFrame2)
        itemFrames.append(itemFrame3)

        counter = 0
        for top in top3lists:
            tk.Label(itemFrames[counter], text=f"{counter + 1}.",font=("Arial", 20, "bold"), fg=FG_COLOR_2, bg=BG_COLOR_3, anchor="e").pack(side=tk.LEFT)
            tk.Label(itemFrames[counter], text=f"👤 {top[0].title()}",font=("Arial", 15),fg=FG_COLOR_2, bg=BG_COLOR_3, anchor="e").pack(side=tk.LEFT, padx=(0, 10))
            tk.Label(itemFrames[counter], text=f"🏆 {top[1]}",font=("Arial", 15),fg=FG_COLOR_2, bg=BG_COLOR_3, anchor="e").pack(side=tk.RIGHT, padx=2)
            tk.Label(itemFrames[counter], text=f"📅 {top[2]}",font=("Arial", 15),fg=FG_COLOR_2, bg=BG_COLOR_3, anchor="e").pack(side=tk.RIGHT, padx=2)
            counter += 1
        
        versus_main_frame = tk.Frame(mainFrame, bg=BG_COLOR_3)
        versus_main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        recentWins_label = tk.Label(versus_main_frame, text="Recent Wins 🥇", font=("Arial", 20, "bold"),bg=BG_COLOR_3, fg=FG_COLOR_2)
        recentWins_label.pack(pady=20)

        versus_listbox = tk.Frame(versus_main_frame, bg=BG_COLOR_3)
        versus_listbox.pack()

        versus_listbox_sub1 = tk.Frame(versus_listbox, bg=BG_COLOR_3)
        versus_listbox_sub1.pack(side=tk.LEFT)

        versus_listbox_sub2 = tk.Frame(versus_listbox, bg=BG_COLOR_3)
        versus_listbox_sub2.pack(side=tk.LEFT)

        versus_listbox_sub3 = tk.Frame(versus_listbox, bg=BG_COLOR_3)
        versus_listbox_sub3.pack(side=tk.RIGHT)

        versus_counter = 0
        for recent in recentLists:
            name1 = recent[0]
            name2 = recent[1]

            if name1 == recent[2]:
                name1 += "🏆"
            elif name2 == recent[2]:
                name2 += "🏆"
            
            # tk.Label(versus_listbox_sub1, text=f"{versus_counter + 1}.",font=("Arial", 20, "bold"), fg=FG_COLOR_2, bg=BG_COLOR_3, justify=tk.LEFT).pack(side=tk.LEFT)
            tk.Label(versus_listbox_sub1, text=f"👤 {name1.title()}",font=("Arial", 15), fg=FG_COLOR_2, bg=BG_COLOR_3, justify="left").pack(anchor="w", padx=5, pady=3)
            tk.Label(versus_listbox_sub2, text=f"VS",font=("Arial", 15, "bold"), fg=FG_COLOR_2, bg=BG_COLOR_3, justify="left").pack(anchor="w", padx=5, pady=3)
            tk.Label(versus_listbox_sub3, text=f"👤 {name2.title()}",font=("Arial", 15), fg=FG_COLOR_2, bg=BG_COLOR_3, justify="left").pack(anchor="w", padx=5, pady=3)
            versus_counter += 1
       
        view_more_btn = tk.Button(self.root, text="View All", command=self.displayRecent, bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, highlightbackground=BTN_HB_COLOR, cursor="hand2")
        view_more_btn.pack(pady=20)
    
    
    # Command Functions

    # Display single player mode
    def singlePlayer(self, Home):
        self.root.destroy()
        PlayerInfo(Home, True)


    # Display Two player mode
    def twoPlayer(self, Home):
        self.root.destroy()
        PlayerInfo(Home, False)
    
    # Display Recent Wins 
    def displayRecent(self):
        self.root.destroy()
        RecentWins(Home)
