import tkinter as tk
from constants import *
from PIL import ImageTk, Image
from onefile import resource_path

class Template:
    def __init__(self, root, bg_color):
        self.root = root
        self.bg_color = bg_color
        self.GameOn = True
    
    def getGameOn(self):
        return self.GameOn
    
    def setGameOn(self, status):
        self.GameOn = status
    
    def getRoot(self):
        return self.root
    
    # Functions
    def displayHome(self, Home):
        self.getGameOn = False
        self.root.destroy()
        Home()
        
    # Main Window
    def mainWindow(self):
        self.root.title(TITLE)
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg=self.bg_color)


    # Navigation Bar
    def navigationBar (self, Home):
        nav_bar = tk.Frame(self.root, bg=self.bg_color, height=30)
        nav_bar.pack(fill=tk.X)

        home_btn = tk.Button(nav_bar, text="Home", command=lambda: self.displayHome(Home), bg=BTN_BG_COLOR, fg=BTN_FG_COLOR, highlightbackground=BTN_HB_COLOR, borderwidth=0, cursor="hand2")
        home_btn.pack(side=tk.LEFT, padx=5, pady=4)

        quizzer_label = tk.Label(nav_bar, text="NuQuizzer", font=("Arial", 20),fg="white", bg=self.bg_color)
        quizzer_label.pack(side=tk.RIGHT, padx=10, pady=4)

    # Title
    def title(self):
        # Main logo image
        logoImage = ImageTk.PhotoImage(Image.open(resource_path("res/imgs/logo1.png")))
        logoLabel =  tk.Label(self.root, image = logoImage, bg=BG_COLOR_3)

        # This next line will create a reference that stops the GC from deleting the object
        logoLabel.image = logoImage 
        logoLabel.pack(pady=(0, 5), fill=tk.X)

    def team (self):
        logoImage = ImageTk.PhotoImage(Image.open(resource_path("res/imgs/team4.2.png")))
        logoLabel =  tk.Label(self.root, image = logoImage, bg=BG_COLOR_5)

        # This next line will create a reference that stops the GC from deleting the object
        logoLabel.image = logoImage 
        logoLabel.pack(fill = tk.BOTH, expand=True)


    # Footer Label
    def footer(self, color="#ef7021"):
        footer_frame = tk.Frame(self.root, bg=color)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        footer_label = tk.Label(footer_frame, text="@ICAT Project 2025", font=("Arial", 15, "italic"), fg=FG_COLOR_2, bg=color)
        footer_label.pack(side=tk.BOTTOM, pady=0)

    def end(self):
        self.root.eval('tk::PlaceWindow . center')
        self.root.mainloop()
        
    
    
