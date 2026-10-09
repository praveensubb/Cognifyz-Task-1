import tkinter as tk
from tkinter import messagebox
import random
import json
import os

STATS_FILE = "stats.json"

class GuessNumberApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎯 Guess the Number")
        
        # Color Palette
        self.bg_color = "#1E1E2E"
        self.card_color = "#313244"
        self.text_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.danger_color = "#f38ba8"
        self.success_color = "#a6e3a1"
        self.warn_color = "#f9e2af"
        
        self.configure(bg=self.bg_color)
        self.center_window(900, 600)
        
        self.stats = self.load_stats()
        
        self.player_name = tk.StringVar()
        self.difficulty = tk.StringVar(value="MEDIUM")
        self.secret_number = 0
        self.max_num = 100
        self.max_attempts = 7
        self.attempts_used = 0
        self.score = 1000
        self.guesses_made = set()
        
        self.container = tk.Frame(self, bg=self.bg_color)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (HomeFrame, GameFrame, ResultFrame, StatsFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("HomeFrame")
        
    def center_window(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def load_stats(self):
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"games_played": 0, "games_won": 0, "games_lost": 0, "best_score": 0}

    def save_stats(self):
        try:
            with open(STATS_FILE, 'w') as f:
                json.dump(self.stats, f)
        except Exception:
            pass

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "StatsFrame":
            frame.update_ui()
        elif page_name == "GameFrame":
            frame.guess_entry.focus_set()

    def start_game(self):
        name = self.player_name.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter your name!")
            return
            
        diff = self.difficulty.get()
        if diff == "EASY":
            self.max_num = 50
            self.max_attempts = 10
        elif diff == "MEDIUM":
            self.max_num = 100
            self.max_attempts = 7
        elif diff == "HARD":
            self.max_num = 500
            self.max_attempts = 6
            
        self.secret_number = random.randint(1, self.max_num)
        self.attempts_used = 0
        self.score = 1000
        self.guesses_made = set()
        
        self.frames["GameFrame"].update_ui_initial()
        self.show_frame("GameFrame")

    def handle_win(self):
        if self.attempts_used == 1:
            self.score += 500
        elif self.attempts_used <= self.max_attempts // 2:
            self.score += 200
        
        self.score = max(100, self.score)
        self.stats['games_played'] += 1
        self.stats['games_won'] += 1
        self.stats['best_score'] = max(self.stats['best_score'], self.score)
        self.save_stats()
        
        self.frames["ResultFrame"].update_ui(True)
        self.show_frame("ResultFrame")
        
    def handle_lose(self):
        self.score = 0
        self.stats['games_played'] += 1
        self.stats['games_lost'] += 1
        self.save_stats()
        
        self.frames["ResultFrame"].update_ui(False)
        self.show_frame("ResultFrame")


class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        
        content = tk.Frame(self, bg=controller.bg_color)
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(content, text="🎯 GUESS THE NUMBER", bg=controller.bg_color, fg=controller.accent_color, font=("Segoe UI", 36, "bold")).pack(pady=(0, 10))
        tk.Label(content, text="Test your guessing skills!", bg=controller.bg_color, fg="#a6adc8", font=("Segoe UI", 16)).pack(pady=(0, 30))
        
        input_frame = tk.Frame(content, bg=controller.bg_color)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Enter your name:", bg=controller.bg_color, fg=controller.text_color, font=("Segoe UI", 14)).pack(side="left", padx=10)
        
        self.name_entry = tk.Entry(input_frame, textvariable=controller.player_name, font=("Segoe UI", 14), width=20, bg=controller.card_color, fg=controller.text_color, insertbackground=controller.text_color, bd=0)
        self.name_entry.pack(side="left", ipady=5, padx=10)
        self.name_entry.bind("<Return>", lambda e: controller.start_game())
        
        diff_frame = tk.LabelFrame(content, text=" Select Difficulty ", bg=controller.bg_color, fg="#a6adc8", font=("Segoe UI", 12), bd=1, padx=20, pady=10)
        diff_frame.pack(pady=20)
        
        for text, val in [("EASY (1-50, 10 attempts)", "EASY"), ("MEDIUM (1-100, 7 attempts)", "MEDIUM"), ("HARD (1-500, 6 attempts)", "HARD")]:
            tk.Radiobutton(diff_frame, text=text, variable=controller.difficulty, value=val, 
                           bg=controller.bg_color, fg=controller.text_color, selectcolor=controller.card_color, 
                           activebackground=controller.bg_color, activeforeground=controller.accent_color, font=("Segoe UI", 12)).pack(anchor="w", pady=5)
        
        btn_frame = tk.Frame(content, bg=controller.bg_color)
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="🚀 START GAME", bg=controller.accent_color, fg="#11111b", font=("Segoe UI", 14, "bold"), 
                  relief="flat", bd=0, padx=20, pady=10, command=controller.start_game, cursor="hand2").pack(side="left", padx=10)
                  
        tk.Button(btn_frame, text="📊 STATISTICS", bg=controller.card_color, fg=controller.text_color, font=("Segoe UI", 14, "bold"), 
                  relief="flat", bd=0, padx=20, pady=10, command=lambda: controller.show_frame("StatsFrame"), cursor="hand2").pack(side="left", padx=10)


class GameFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        
        top_bar = tk.Frame(self, bg=controller.card_color, height=50)
        top_bar.pack(fill="x")
        
        self.info_label = tk.Label(top_bar, text="", bg=controller.card_color, fg=controller.text_color, font=("Segoe UI", 12))
        self.info_label.pack(pady=10)
        
        content = tk.Frame(self, bg=controller.bg_color)
        content.pack(expand=True, fill="both", pady=30)
        
        self.attempts_lbl = tk.Label(content, text="", bg=controller.bg_color, fg="#a6adc8", font=("Segoe UI", 16))
        self.attempts_lbl.pack(pady=10)
        
        self.score_lbl = tk.Label(content, text="", bg=controller.bg_color, fg=controller.accent_color, font=("Segoe UI", 16, "bold"))
        self.score_lbl.pack(pady=10)
        
        self.hint_label = tk.Label(content, text="", bg=controller.bg_color, fg=controller.warn_color, font=("Segoe UI", 14, "italic"))
        self.hint_label.pack(pady=15)
        
        entry_frame = tk.Frame(content, bg=controller.bg_color)
        entry_frame.pack(pady=20)
        
        self.guess_entry = tk.Entry(entry_frame, font=("Segoe UI", 24), width=10, justify="center", bg=controller.card_color, fg=controller.text_color, insertbackground=controller.text_color, bd=0)
        self.guess_entry.pack(side="left", padx=10, ipady=10)
        self.guess_entry.bind("<Return>", self.on_submit)
        
        tk.Button(entry_frame, text="🎯 SUBMIT", font=("Segoe UI", 14, "bold"), bg=controller.success_color, fg="#11111b", bd=0, padx=20, pady=10, command=self.on_submit, cursor="hand2").pack(side="left")
        
        self.feedback_lbl = tk.Label(content, text="", bg=controller.bg_color, fg=controller.text_color, font=("Segoe UI", 16))
        self.feedback_lbl.pack(pady=30)
        
    def update_ui_initial(self):
        c = self.controller
        self.info_label.config(text=f"👤 {c.player_name.get()}  |  🎚️ {c.difficulty.get()}  |  🔢 Range: 1 - {c.max_num}")
        self.attempts_lbl.config(text=f"Attempts Remaining: {c.max_attempts}")
        self.score_lbl.config(text=f"Current Score: {c.score}")
        self.hint_label.config(text="")
        self.feedback_lbl.config(text="Enter a number to start guessing!", fg=c.text_color)
        self.guess_entry.delete(0, tk.END)
        
    def on_submit(self, event=None):
        guess_str = self.guess_entry.get().strip()
        self.guess_entry.delete(0, tk.END)
        
        if not guess_str:
            self.show_feedback("Please enter a number.", "warning")
            return
            
        try:
            guess = int(guess_str)
        except ValueError:
            self.show_feedback("❌ Invalid! Enter numbers only.", "error")
            return
            
        c = self.controller
        if guess < 1 or guess > c.max_num:
            self.show_feedback(f"❌ Out of range (1-{c.max_num})!", "error")
            return
            
        if guess in c.guesses_made:
            self.show_feedback("⚠️ You already guessed that number!", "warning")
            return
            
        c.guesses_made.add(guess)
        c.attempts_used += 1
        
        if guess == c.secret_number:
            c.handle_win()
        else:
            c.score = max(0, c.score - 100)
            if c.attempts_used >= c.max_attempts:
                c.handle_lose()
            else:
                feedback = "❌ Too High! Try a lower number." if guess > c.secret_number else "❌ Too Low! Try a higher number."
                self.show_feedback(feedback, "error")
                
                rem = c.max_attempts - c.attempts_used
                self.attempts_lbl.config(text=f"Attempts Remaining: {rem}")
                self.score_lbl.config(text=f"Current Score: {c.score}")
                self.check_hints()

    def check_hints(self):
        c = self.controller
        wrong = c.attempts_used
        if wrong == 2:
            hint = "EVEN" if c.secret_number % 2 == 0 else "ODD"
            self.hint_label.config(text=f"💡 Hint: The number is {hint}.")
        elif wrong == 4:
            low = max(1, c.secret_number - random.randint(5, 12))
            high = min(c.max_num, c.secret_number + random.randint(5, 12))
            self.hint_label.config(text=f"💡 Hint: It is between {low} and {high}.")

    def show_feedback(self, msg, mtype):
        self.feedback_lbl.config(text=msg)
        c = self.controller
        if mtype == "error":
            self.feedback_lbl.config(fg=c.danger_color)
        elif mtype == "warning":
            self.feedback_lbl.config(fg=c.warn_color)
        else:
            self.feedback_lbl.config(fg=c.success_color)


class ResultFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        
        content = tk.Frame(self, bg=controller.bg_color)
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        self.title_lbl = tk.Label(content, text="", bg=controller.bg_color, font=("Segoe UI", 36, "bold"))
        self.title_lbl.pack(pady=20)
        
        self.msg_lbl = tk.Label(content, text="", bg=controller.bg_color, fg=controller.text_color, font=("Segoe UI", 18))
        self.msg_lbl.pack(pady=10)
        
        self.stats_lbl = tk.Label(content, text="", bg=controller.bg_color, fg=controller.accent_color, font=("Segoe UI", 16), justify="center")
        self.stats_lbl.pack(pady=20)
        
        btn_frame = tk.Frame(content, bg=controller.bg_color)
        btn_frame.pack(pady=30)
        
        self.play_again_btn = tk.Button(btn_frame, text="", bg=controller.accent_color, fg="#11111b", font=("Segoe UI", 14, "bold"), 
                                        relief="flat", bd=0, padx=15, pady=10, command=controller.start_game, cursor="hand2")
        self.play_again_btn.pack(side="left", padx=10)
        
        tk.Button(btn_frame, text="⚙️ CHANGE DIFFICULTY", bg=controller.card_color, fg=controller.text_color, font=("Segoe UI", 14, "bold"), 
                  relief="flat", bd=0, padx=15, pady=10, command=lambda: controller.show_frame("HomeFrame"), cursor="hand2").pack(side="left", padx=10)
                  
        tk.Button(btn_frame, text="❌ EXIT", bg=controller.danger_color, fg="#11111b", font=("Segoe UI", 14, "bold"), 
                  relief="flat", bd=0, padx=15, pady=10, command=controller.destroy, cursor="hand2").pack(side="left", padx=10)

    def update_ui(self, won):
        c = self.controller
        if won:
            self.title_lbl.config(text="🎉 CONGRATULATIONS!", fg=c.success_color)
            self.msg_lbl.config(text=f"Great job, {c.player_name.get()}! You guessed it!")
            self.play_again_btn.config(text="🔄 PLAY AGAIN")
        else:
            self.title_lbl.config(text="😔 GAME OVER", fg=c.danger_color)
            self.msg_lbl.config(text="You ran out of attempts!")
            self.play_again_btn.config(text="🔄 TRY AGAIN")
            
        self.stats_lbl.config(text=f"Secret Number: {c.secret_number}\nAttempts Used: {c.attempts_used}\nFinal Score: {c.score}")


class StatsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        
        content = tk.Frame(self, bg=controller.bg_color)
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(content, text="📊 STATISTICS", bg=controller.bg_color, fg=controller.accent_color, font=("Segoe UI", 32, "bold")).pack(pady=20)
        
        card = tk.Frame(content, bg=controller.card_color, padx=40, pady=40)
        card.pack(pady=20)
        
        self.stats_text = tk.Label(card, text="", bg=controller.card_color, fg=controller.text_color, font=("Segoe UI", 18), justify="left")
        self.stats_text.pack()
        
        tk.Button(content, text="⬅️ BACK TO HOME", bg=controller.card_color, fg=controller.text_color, font=("Segoe UI", 14, "bold"), 
                  relief="flat", bd=0, padx=20, pady=10, command=lambda: controller.show_frame("HomeFrame"), cursor="hand2").pack(pady=30)
                  
    def update_ui(self):
        stats = self.controller.stats
        played = stats['games_played']
        won = stats['games_won']
        lost = stats['games_lost']
        best = stats['best_score']
        
        win_rate = (won / played * 100) if played > 0 else 0
        
        text = f"🎮 Games Played: {played}\n\n"
        text += f"🏆 Games Won: {won}\n\n"
        text += f"💀 Games Lost: {lost}\n\n"
        text += f"📈 Win Rate: {win_rate:.1f}%\n\n"
        text += f"⭐ Best Score: {best}"
        
        self.stats_text.config(text=text)

if __name__ == "__main__":
    app = GuessNumberApp()
    app.mainloop()
