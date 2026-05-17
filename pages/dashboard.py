import customtkinter as ctk
from datetime import datetime
import random

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0A0E27")
        
        quotes = [
            "Focus on progress, not perfection.",
            "You're doing great! Keep it up!",
            "Every minute counts!",
            "Stay productive, stay focused!",
            "Never give up!",
            "Small steps lead to big achievements.",
            "Nothing is impossible, the word itself says 'I'm possible'!",
            "Every step matters, you can do it!",
            "Believe in yourself and all that you are.",
            "Always trust yourself and your abilities."
        ]
        
        # Create grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # row 0: title (fixed), row 1: clock, row 2: motivation
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Project title above the clock card (separate, large and bold)
        title_label = ctk.CTkLabel(
            self,
            text="FocusFlow",
            font=("Segoe UI", 48, "bold"),
            text_color="#E0E7FF"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 5), sticky="n")

        # Clock card (keep layout same)
        clock_card = ctk.CTkFrame(self, fg_color="#1A1F3A", corner_radius=20)
        clock_card.grid(row=1, column=0, padx=15, pady=15, sticky="nsew", columnspan=2)

        time_label = ctk.CTkLabel(
            clock_card,
            text="",
            font=("Segoe UI", 72, "bold"),
            text_color="#A78BFA"
        )
        time_label.pack(pady=40)
        
        def update_clock():
            current_time = datetime.now().strftime("%H:%M:%S")
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            time_label.configure(text=f"{current_time}\n{current_date}")
            self.after(1000, update_clock)
        
        update_clock()
        
        # Motivation card
        motivate_card = ctk.CTkFrame(self, fg_color="#1A1F3A", corner_radius=20)
        motivate_card.grid(row=2, column=0, columnspan=2, padx=15, pady=15, sticky="nsew")
        
        quote_label = ctk.CTkLabel(
            motivate_card,
            text=f"💡 {random.choice(quotes)}",
            font=("Segoe UI", 18),
            text_color="#E0E7FF",
            wraplength=500
        )
        quote_label.pack(pady=30, padx=30)
