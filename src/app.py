import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from constants import *
import time
from PIL import ImageTk, Image
from mcqs import MCQS
import time
import threading
from filehandler import FileHandler
from onefile import resource_path
import random

class App:
    ##############      Constructor      ##############
    def __init__(self, root, bg_color, Home, template, player1_name,player2_name="",single= True):
        
        # Attributes
        self.root = root
        self.Home = Home
        self.template = template
        
        self.single = single
        self.bg_color = bg_color

        self.csvhandler = FileHandler() 

        # Timer 
        self.MCQ_Counter = SINGLE_MCQ_TIMER
        self.full_time = FULL_TIME

        # PLayer 1
        self.player1_name = player1_name
        self.player1_score = 0
        
        # Player 2
        self.player2_name = player2_name
        self.player2_score = 0

        # Booleans for Logic 
        self.optionClicked = False
        

        # Threads
        self.overall_timer_thread = threading.Thread(target=self.OverallTimeCounter)
        self.progressBarThread = threading.Thread(target=self.progressBarTimer, args=[])
        self.mcq_thread = threading.Thread(target=self.mcqTimer, args=[])

        # Key Event
        if self.single is False:
            self.winner = ""
            self.loser = ""
            self.draw = False
            self.checkTwoPlayerScore()
        
    ##############      Functions      ##############

    ### Get Functions 
    def getPlayer1Score(self):
        return self.player1_score
    
    def getFileName(self):
        return self.generateMcqs.getFileName()
    
    def getQustion(self, mcqs):
        return self.cleanQuestion(mcqs.get('Question'))
    
    def getOptions(self, mcqs):
        mcqsList = []
        mcqsList.append(mcqs.get('OptionA'))
        mcqsList.append(mcqs.get('OptionB'))
        mcqsList.append(mcqs.get('OptionC'))
        mcqsList.append(mcqs.get('OptionD'))
        return mcqsList
    
    def getAnswer(self, mcqs):
        return mcqs.get("Answer")
    
    ### Helper Functions
    # Cleans the Question by adding returns after 40 characters
    def cleanQuestion(self, question):
        count = 0
        newQuestion = ""
        for character in question:
            if count > 40:
                if character == ' ':
                    character = '\n'
                    count = 0
            else: 
                count += 1
            newQuestion += character
        return newQuestion
    
    # Display images with the following parameters
    def displayImages(self, frame, url, color, customSide=tk.LEFT):
        logoImage = ImageTk.PhotoImage(Image.open(url))
        logoLabel =  tk.Label(frame, image = logoImage, bg=color)

        # This next line will create a reference that stops the GC from deleting the object
        logoLabel.image = logoImage 
        logoLabel.pack(side=customSide, pady=0)
    
    # Store Data to csv file in stored folder
    def saveData(self):
        if self.single is True: 
            self.csvhandler.single_user_input(self.player1_name, self.player1_score)
        else:
            self.csvhandler.twoPlayer_user_input(self.player1_name, self.player2_name, self.winner, self.draw)
  
    ### MCQS Functions
    # Generate Random MCQ
    def generateMCQ(self):
        self.generateMcqs = MCQS()
        mcqs = self.generateMcqs.getRandomMCQ()
        return mcqs
    
    # Fetches data for mcqs
    def getMCQs(self):
        # MCQs Attributes
        try:
            mcq = self.generateMCQ() 
            fileName = self.getFileName()
        except:
            self.getMCQs()
        
        mcq_question = self.getQustion(mcq)
        mcq_options = self.getOptions(mcq)
        self.mcq_answer = self.getAnswer(mcq)
        self.mcqs(file=fileName, question=mcq_question, answer= self.mcq_answer, optionList=mcq_options, single=self.single)


    # Destroy mcq for new MCQ frame
    def destroyMCQFrame(self):
        self.MCQs_frame.destroy()
    
    # MCQ Frame Thread
    def mcqThreadStart(self):
        # MCQ Frame and Thread
        self.mcq_thread.start()

    # MCQ timer for thread
    def mcqTimer(self):
        try:
            while self.template.getGameOn():
                    self.getMCQs()
                    self.mcqSleep(SINGLE_MCQ_TIMER)
                    # time.sleep(SINGLE_MCQ_TIMER)
                    self.destroyMCQFrame()
                    self.progressBarRestart()
                    if self.optionClicked is False:
                        self.removePlayer1Score(2)
                        if self.single is False:
                            self.removePlayer2Score(2)
                    else:
                        self.optionClicked = False
            self.MCQs_frame.destroy()
        except:
            pass
        

    # MCQ Delay function
    def mcqSleep(self, val):
        start_time = time.monotonic()
        delay = val  # delay in seconds
        runLoop = True
        while runLoop:
            if self.template.getGameOn() is False:
                break
            current_time = time.monotonic()
            elapsed_time = current_time - start_time            
            if elapsed_time >= delay:
                runLoop = False
            elif self.optionClicked is True:
                runLoop = False
    
    
    ### Progress Bar 
    # Removes -1 from the progress bar
    def progressBarStart(self):
        self.progressbar['value'] -= 1

    # Resets the Progress Bar
    def progressBarRestart(self):
        self.progressbar['value'] = SINGLE_MCQ_TIMER
    
    # Starts the progress bar thread 
    def progressBarThreadStart(self):
        self.progressBar()
        self.progressBarThread.start()

    # Thread starts the timer and once done the frame is destroyed        
    def progressBarTimer(self):
        try:
            while self.template.getGameOn():
                self.progressBarStart()
                time.sleep(1)
            self.progressbar.destroy()
        except:
            pass
        

    ### Score 
    # Add points to player 1
    def addPlayer1Score(self):
        self.player1_score += 10
        self.score1_label.config(text=self.player1_score)
    
    # Remove points from player 1
    def removePlayer1Score(self, val):
        if self.player1_score > 0:
            self.player1_score -= val
            self.score1_label.config(text=self.player1_score)
    
    # Add Points to Player 2
    def addPlayer2Score(self):
        self.player2_score += 10
        self.score2_label.config(text=self.player2_score)
    
    # Remove points from player 2
    def removePlayer2Score(self, val):
        if self.player2_score > 0:
            self.player2_score -= val
            self.score2_label.config(text=self.player2_score)
    
    # Single Player: Checks answer if correct user scores else score is decreased
    def checkScore(self, choosenOption, answer):
        if self.single is True:
            if choosenOption == answer:
                self.addPlayer1Score()
            else:
                self.removePlayer1Score(5)
            self.optionClicked = True
    
    def checkTwoPlayerScore(self):
        self.root.bind('<KeyPress>', self.key_press)
    

    def key_press(self, e):
        
        if e.keysym == PLAYER_1_A:
            # Player 1: A
            convertedKey = self.convertKey(e.keysym)
            self.checkTwoPlayerAnswer(convertedKey, 1)
            self.optionClicked = True
        elif e.keysym == PLAYER_1_B:
            # Player 1: B
            convertedKey = self.convertKey(e.keysym)
            self.checkTwoPlayerAnswer(convertedKey, 1)
            self.optionClicked = True
        elif e.keysym == PLAYER_1_C:
            # Player 1: C
            convertedKey = self.convertKey(e.keysym)
            self.checkTwoPlayerAnswer(convertedKey, 1)
            self.optionClicked = True
        elif e.keysym == PLAYER_1_D:
            # Player 1: D
            convertedKey = self.convertKey(e.keysym)
            self.checkTwoPlayerAnswer(convertedKey, 1)
            self.optionClicked = True
        elif e.keysym == PLAYER_2_A:
            # Player 2: A
            convertedKey = self.convertKey(e.keysym)
            self.checkTwoPlayerAnswer(convertedKey, 2)
            self.optionClicked = True
        elif e.keysym == PLAYER_2_B:
            # Player 2: B
            convertedKey = self.convertKey(e.keysym)
            self.checkTwoPlayerAnswer(convertedKey, 2)
            self.optionClicked = True
        elif e.keysym == PLAYER_2_C:
            # Player 2: c
            convertedKey = self.convertKey(e.keysym)
            self.checkTwoPlayerAnswer(convertedKey, 2)
            self.optionClicked = True
        elif e.keysym == PLAYER_2_D:
            # Player 2: D
            convertedKey = self.convertKey(e.keysym)
            self.checkTwoPlayerAnswer(convertedKey, 2)
            self.optionClicked = True

    def convertKey(self, key):
        answer_dictionary =  {
            "1": 'A',
            "2": 'B',
            "3": 'C',
            "4": 'D',
            "7": 'A',
            "8": 'B',
            "9": 'C',
            "0": 'D'
        }
        return answer_dictionary.get(key)
    
    def checkTwoPlayerAnswer(self, optionChoosen, playerNumber):
        if optionChoosen == self.answer:
            if playerNumber == 1:
                self.addPlayer1Score()
            elif playerNumber == 2:
                self.addPlayer2Score()
        else:
            if playerNumber == 1:
                self.removePlayer1Score(5)
            elif playerNumber == 2:
                self.removePlayer2Score(5)
    
    def checkWinner(self):
        if self.player1_score > self.player2_score:
            self.winner = self.player1_name
            self.loser = self.player2_name
            self.draw = False
        elif self.player1_score < self.player2_score:
            self.winner = self.player2_name
            self.loser = self.player1_name
            self.draw = False
        else:
            self.draw = True
    
    ### Overall Timer
    # Overall Timer Thread
    def OverallTimerThread(self):
        self.overall_timer_thread.start()
    
    # Counter for Overall Timer
    def OverallTimeCounter(self):
        try:
            while self.full_time != 0:
                self.full_time -= 1
                time.sleep(1)
                self.overall_time_label.config(text=self.full_time)
            self.overall_time_frame.destroy()
            self.template.setGameOn(False)
            self.displayScore()
            self.saveData()
            time.sleep(0.5)
            self.displayTotalScore()
            time.sleep(0.5)
            self.DisplayRestart()
        except:
            pass
        
    
    # Function to save name, score and date
    
    
    ##############      Frames      ##############

    # MCQs Frame
    def mcqs(self, file, question, answer, optionList=[], single=True):
        self.answer = answer

        self.MCQs_frame = tk.Frame(self.root, bg=BG_COLOR_3)
        self.MCQs_frame.pack(fill=tk.BOTH)

        question_label = tk.Label(self.MCQs_frame, text=question, font=("Arial", 25), fg=FG_COLOR_2, bg=BG_COLOR_3)
        question_label.pack(pady=25, fill=tk.X)

        if single is True:
            A = 'A'
            B = 'B'
            C = 'C'
            D = 'D'
        else:
            A = 'A2'
            B = 'B2'
            C = 'C2'
            D = 'D2'
              
        # MCQ Image 
        self.mcq_image(self.MCQs_frame, file)

        # Option 1
        self.mcq_option(self.MCQs_frame, resource_path(f"res/options/{A}.png"), optionList[0],'A' ,answer)
        
        # Option 2
        self.mcq_option(self.MCQs_frame, resource_path(f"res/options/{B}.png"), optionList[1], 'B' ,answer)

        # Option C
        self.mcq_option(self.MCQs_frame, resource_path(f"res/options/{C}.png"), optionList[2], 'C' ,answer)

        # Option D
        self.mcq_option(self.MCQs_frame, resource_path(f"res/options/{D}.png"), optionList[3], 'D' ,answer)

    # Options
    def mcq_option(self, MCQs_frame, imagePath, option_text, choosen_option, answer):
        option_frame = tk.Frame(MCQs_frame, bg=BG_COLOR_3)
        option_frame.pack()

        self.displayImages(frame=option_frame, url=imagePath, color=BG_COLOR_3)

        option = tk.Button(option_frame, command=lambda: self.checkScore(choosen_option, answer),text=option_text, highlightbackground=BG_COLOR_3, fg=BG_COLOR_3, bd=0, cursor="hand2", width=50, height=2)
        option.pack(padx=10, pady=15, side=tk.LEFT)

    # Display MCQ top general image
    def mcq_image(self, frame, filename):
        main_frame = tk.Frame(frame, bg=BG_COLOR_3)
        main_frame.pack(fill=tk.X)

        logoImage = ImageTk.PhotoImage(Image.open(resource_path(f"res/mcqs-imgs/{filename}.png")))
        logoLabel =  tk.Label(main_frame, image = logoImage, bg=BG_COLOR_3)

        # This next line will create a reference that stops the GC from deleting the object
        logoLabel.image = logoImage 
        logoLabel.pack(fill = tk.BOTH, pady=(20, 10), expand=True)


    # Progress Bar Frame
    def progressBar(self):
        progress_frame = tk.Frame(self.root, bg=BG_COLOR_3)
        progress_frame.pack(side=tk.BOTTOM,pady=(0,20))

        self.progressbar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=300,  mode="determinate", max=SINGLE_MCQ_TIMER)
        self.progressbar['value'] = SINGLE_MCQ_TIMER
        self.progressbar.pack(padx=20)
    
    
    # Score Frame 
    def score(self,single=True):
        # Main Score Frame
        score_frame = tk.Frame(self.root, bg=BG_COLOR_5)
        score_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Sub Score Frame 
        sub_score_frame = tk.Frame(score_frame, bg=BG_COLOR_5, highlightthickness=2, highlightcolor=BG_COLOR_4)
        sub_score_frame.pack(side=tk.RIGHT)

        # Player Names Frame + Score Frame
        players = tk.Frame(sub_score_frame, bg=BG_COLOR_5)
        players.pack(side=tk.RIGHT)

        # Player 1
        player1 = tk.Frame(players, bg=BG_COLOR_5)
        player1.pack(side=tk.TOP)

        # Player 1 Name Label
        name_label = tk.Label(player1, text=self.player1_name, fg=BG_COLOR_4, bg=BG_COLOR_5)
        name_label.pack(side=tk.LEFT)

        # Player 1 Score Label
        self.score1_label = tk.Label (player1, text=self.player1_score, fg=BG_COLOR_4, bg=BG_COLOR_5)
        self.score1_label.pack(side=tk.LEFT, padx=(0, 20))

        # If 2 player mode is choosen
        if self.single is False:
            # Player 2
            player2 = tk.Frame(players, bg=BG_COLOR_5)
            player2.pack(side=tk.BOTTOM)

            # Player 2 Name Label
            name2_label = tk.Label(player2, text=self.player2_name, fg=BG_COLOR_4, bg=BG_COLOR_5)
            name2_label.pack(side=tk.LEFT)

            # Player 1 Score Label
            self.score2_label = tk.Label (player2, text=self.player2_score, fg=BG_COLOR_4, bg=BG_COLOR_5)
            self.score2_label.pack(side=tk.LEFT, padx=(0, 20))

        # Image
        self.displayImages(sub_score_frame, resource_path("res/app-imgs/score.png"), color=BG_COLOR_5, customSide=tk.LEFT)

    # OverAll Timer Frame
    def overallTimer(self):
        self.overall_time_frame = tk.Frame(self.root, bg=BG_COLOR_3)
        self.overall_time_frame.pack()

        self.displayImages(self.overall_time_frame, resource_path("res/app-imgs/timer-3.png"), BG_COLOR_3)

        self.overall_time_label = tk.Label(self.overall_time_frame, text=self.full_time, fg=FG_COLOR_2, bg=BG_COLOR_5 ,font=("Arial", 15))
        self.overall_time_label.pack(side=tk.RIGHT)
        self.OverallTimerThread()
    
    def DisplayRestart(self):
        restart_label = tk.Label(self.root, text="Click on Home 🏠 Button to restart.", bg=BG_COLOR_5,fg=BG_COLOR_4, font=("Arial", 20))
        restart_label.pack(pady=20)
        
    def displayScore(self):
        if self.single is True:
            messagebox.showinfo("Score 🎊", f"{self.player1_name} your score is {self.player1_score}")  
        else:
            self.checkWinner()
            if self.draw:
                phrase = self.drawPhrases()
                messagebox.showinfo("Draw!",phrase)
            else:
                phrase  = self.winnerPhrases()
                messagebox.showinfo("Congrats 🎊", f"Congrats, {self.winner} \n {phrase}")  

    def winnerPhrases(self):
        winner_phrases = [
            "Victory is sweet!",
            "Champion of the day!",
            "Well played, you're the ultimate winner!",
            "You crushed it—congratulations!",
            "The trophy is yours!",
            "Victory never looked so good!",
            "You've earned the crown!",
            "Game over, and you came out on top!",
            "The champion has emerged!"
        ]
        # Randomly pick a phrase
        random_phrase = random.choice(winner_phrases)

        return random_phrase
    
    def drawPhrases(self):
        draw_phrases = [
            "It's a tie!",
            "No winner this time!",
            "A draw, both played well!",
            "Neither side conquered today!",
            "A perfect balance!",
            "A battle for the ages, ending in a draw!",
            "Equal in skill, equal in victory!",
            "What a close call—it's a draw!",
            "Both sides are winners today!",
            "A deadlock to remember!"
        ]
        random_phrase = random.choice(draw_phrases)
        return random_phrase


    # Total Score Frame
    def displayTotalScore(self):
        total_score_frame = tk.Frame(self.root, bg=BG_COLOR_3)
        total_score_frame.pack()

        frame1 = tk.Frame(self.root, bg=BG_COLOR_3)
        frame1.pack(fill=tk.X)

        congrats = tk.Label(frame1, text="🎊", font=("Arial", 35),bg=BG_COLOR_3)
        congrats.pack(pady=40)

        frame2 = tk.Frame(self.root, bg=BG_COLOR_3)
        frame2.pack()
        if self.single is True:
            player1_name_label = tk.Label(frame2, text=self.player1_name, font=("Arial", 20),bg=BG_COLOR_3, fg=FG_COLOR_2)
            player1_name_label.pack(side=tk.LEFT)

            player1_score_label = tk.Label(frame2, text=self.player1_score, font=("Arial", 20),bg=BG_COLOR_3, fg=FG_COLOR_2)
            player1_score_label.pack(side=tk.RIGHT)
        else:
            tk.Label(frame2, text=f"{self.player1_name} Score: {self.player1_score}", font=("Arial", 20),bg=BG_COLOR_3, fg=FG_COLOR_2).pack()
            tk.Label(frame2, text=f"{self.player2_name} Score: {self.player2_score}", font=("Arial", 20),bg=BG_COLOR_3, fg=FG_COLOR_2).pack(pady=(5, 15))
            if self.draw:
                tk.Label(frame2, text=f"A draw, both played well!!", font=("Arial", 20),bg=BG_COLOR_3, fg=FG_COLOR_2).pack()
            else:
                tk.Label(frame2, text=f"Congrats, {self.winner} ✨ \n {self.loser} better luck next time!", font=("Arial", 20),bg=BG_COLOR_3, fg=FG_COLOR_2).pack()

