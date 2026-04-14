import tkinter as tk
from constants import *
from template import Template
from filehandler import FileHandler

class RecentWins:
    def __init__(self, Home):
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

        # Team
        # template.team()        

        # Footer Label
        template.footer()
        template.end()

    #Frames Functions
                
    #ScoreBoard
    def scoreBoard(self):
        top3lists = self.csvhandler.fetchTopAll()
        recentLists = self.csvhandler.fetchRecentAll()

        mainFrame = tk.Frame(self.root, bg=BG_COLOR_3)
        mainFrame.pack(fill=tk.BOTH)

        top_players_frame = tk.Frame(mainFrame, bg=BG_COLOR_3)
        top_players_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        top_players_subframe = self.scrollBarFunc(top_players_frame)

        top_players_label = tk.Label(top_players_subframe, text="Top Players 🏅", font=("Arial", 20, "bold"),bg=BG_COLOR_3, fg=FG_COLOR_2)
        top_players_label.pack(pady=20)

        listbox = tk.Frame(top_players_subframe, bg=BG_COLOR_3)
        listbox.pack()
        
        listbox_sub1 = tk.Frame(listbox, bg=BG_COLOR_3)
        listbox_sub1.pack(side=tk.LEFT)

        listbox_sub2 = tk.Frame(listbox, bg=BG_COLOR_3)
        listbox_sub2.pack(side=tk.LEFT)

        listbox_sub3 = tk.Frame(listbox, bg=BG_COLOR_3)
        listbox_sub3.pack(side=tk.RIGHT)

        listbox_sub4 = tk.Frame(listbox, bg=BG_COLOR_3)
        listbox_sub4.pack(side=tk.RIGHT)

        counter = 0
        for top in top3lists:
            tk.Label(listbox_sub1, text=f"{counter + 1}.",font=("Arial", 15, "bold"), fg=FG_COLOR_2, bg=BG_COLOR_3, justify="left").pack(anchor="w", padx=1, pady=1)
            tk.Label(listbox_sub2, text=f"👤 {top[0].title()}",font=("Arial", 15),fg=FG_COLOR_2, bg=BG_COLOR_3, justify="left").pack(anchor="w", padx=1, pady=1)
            tk.Label(listbox_sub3, text=f"🏆 {top[1]}",font=("Arial", 15),fg=FG_COLOR_2, bg=BG_COLOR_3, justify="left").pack(anchor="w", padx=1, pady=1)
            tk.Label(listbox_sub4, text=f"📅 {top[2]}",font=("Arial", 15),fg=FG_COLOR_2, bg=BG_COLOR_3, justify="left").pack(anchor="w", padx=1, pady=1)
            counter += 1

        
        # Versus Frames
        
        versus_main_frame = tk.Frame(mainFrame, bg=BG_COLOR_3)
        versus_main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        versus_sub_frame = self.scrollBarFunc(versus_main_frame)

        recentWins_label = tk.Label(versus_sub_frame, text="Recent Wins 🥇", font=("Arial", 20, "bold"),bg=BG_COLOR_3, fg=FG_COLOR_2)
        recentWins_label.pack(pady=20)

        versus_listbox = tk.Frame(versus_sub_frame, bg=BG_COLOR_3)
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
            
            tk.Label(versus_listbox_sub1, text=f"👤 {name1.title()}",font=("Arial", 15), fg=FG_COLOR_2, bg=BG_COLOR_3, justify="left").pack(anchor="w", padx=5, pady=3)
            tk.Label(versus_listbox_sub2, text=f"VS",font=("Arial", 15, "bold"), fg=FG_COLOR_2, bg=BG_COLOR_3, justify="left").pack(anchor="w", padx=5, pady=3)
            tk.Label(versus_listbox_sub3, text=f"👤 {name2.title()}",font=("Arial", 15), fg=FG_COLOR_2, bg=BG_COLOR_3, justify="left").pack(anchor="w", padx=5, pady=3)
            versus_counter += 1
    
    def scrollBarFunc(self, mainFrame):  
        # Canvas that will hold the sub_main
        canvas = tk.Canvas(mainFrame, bg=BG_COLOR_3, borderwidth=0, highlightthickness=0, height=500)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar attached to the canvas
        scrollbar = tk.Scrollbar(mainFrame, orient="vertical",command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to work with the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create the sub_main inside the canvas
        sub_main = tk.Frame(canvas, bg=BG_COLOR_3)
        canvas.create_window((0, 0), window=sub_main, anchor="nw")

        # Update the scrollregion of the canvas to match the size of the versus_main_frame
        def onFrameConfigure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Bind the event to update the scroll region
        sub_main.bind("<Configure>", onFrameConfigure)

        return sub_main
