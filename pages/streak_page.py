import customtkinter as ctk
import json
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
STREAK_FILE = os.path.join(DATA_DIR, "streak.json")

class StreakPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0A0E27")

        self.streak_data = self.load_streak_data()
        
        # Store references to update later
        self.streak_number_label = None
        self.last_date_label = None
        self.best_label = None
        self.status_label = None

        # Main card
        main_card = ctk.CTkFrame(self, fg_color="#1A1F3A", corner_radius=20)
        main_card.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            main_card,
            text="Daily Streak 🔥",
            font=("Segoe UI", 34, "bold"),
            text_color="#A78BFA"
        )
        title.pack(pady=30, anchor="w", padx=20)

        # Streak count display (large)
        streak_count_frame = ctk.CTkFrame(main_card, fg_color="#2D3250", corner_radius=15)
        streak_count_frame.pack(pady=20, padx=20, fill="x")

        streak_label = ctk.CTkLabel(
            streak_count_frame,
            text="Current Streak",
            font=("Segoe UI", 16),
            text_color="#B0B3B3"
        )
        streak_label.pack(pady=(20, 5), padx=20)

        current_streak = self.streak_data.get("current_streak", 0)
        self.streak_number_label = ctk.CTkLabel(
            streak_count_frame,
            text=str(current_streak),
            font=("Segoe UI", 72, "bold"),
            text_color="#F0C21E"
        )
        self.streak_number_label.pack(pady=(5, 20), padx=20)

        # Last study date
        last_date_str = self.streak_data.get("last_study_date", "Never")
        self.last_date_label = ctk.CTkLabel(
            main_card,
            text=f"Last study: {last_date_str}",
            font=("Segoe UI", 14),
            text_color="#B0B3B3"
        )
        self.last_date_label.pack(pady=10, padx=20, anchor="w")

        # Best streak
        best_streak = self.streak_data.get("best_streak", 0)
        self.best_label = ctk.CTkLabel(
            main_card,
            text=f"Best streak: {best_streak} days",
            font=("Segoe UI", 14),
            text_color="#B0B3B3"
        )
        self.best_label.pack(pady=10, padx=20, anchor="w")

        # Mark today as studied button
        mark_btn = ctk.CTkButton(
            main_card,
            text="Mark Today as Studied ✓",
            command=self.mark_today_studied,
            fg_color="#A78BFA",
            hover_color="#9370DB",
            font=("Segoe UI", 14, "bold"),
            height=50
        )
        mark_btn.pack(pady=20, padx=20, fill="x")

        # Status message
        self.status_label = ctk.CTkLabel(
            main_card,
            text="",
            font=("Segoe UI", 12),
            text_color="#10B981"
        )
        self.status_label.pack(pady=10, padx=20, anchor="w")

        # Reset streak button (smaller)
        reset_btn = ctk.CTkButton(
            main_card,
            text="Reset Streak",
            command=self.reset_streak,
            fg_color="#EF4444",
            hover_color="#DC2626",
            font=("Segoe UI", 12),
            height=40
        )
        reset_btn.pack(pady=10, padx=20, fill="x")

    def load_streak_data(self):
        """Load streak data from JSON file"""
        default_data = {
            "current_streak": 0,
            "best_streak": 0,
            "last_study_date": "Never",
            "total_study_days": 0
        }
        
        if os.path.exists(STREAK_FILE):
            try:
                with open(STREAK_FILE, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    return {**default_data, **data}
            except Exception:
                pass
        
        return default_data

    def save_streak_data(self):
        """Save streak data to JSON file"""
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(STREAK_FILE, "w", encoding="utf-8") as file:
            json.dump(self.streak_data, file, indent=2)

    def mark_today_studied(self):
        """Mark today as studied and update streak"""
        today = datetime.now().strftime("%Y-%m-%d")
        last_date = self.streak_data.get("last_study_date", "Never")

        if last_date == today:
            self.status_label.configure(text="✓ Already marked for today!", text_color="#10B981")
            return

        # Calculate streak
        if last_date != "Never":
            try:
                last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")
                today_obj = datetime.strptime(today, "%Y-%m-%d")
                days_diff = (today_obj - last_date_obj).days

                if days_diff == 1:
                    # Consecutive day
                    self.streak_data["current_streak"] += 1
                elif days_diff > 1:
                    # Streak broken, reset to 1
                    self.streak_data["current_streak"] = 1
                else:
                    # Same day, do nothing
                    return
            except Exception:
                self.streak_data["current_streak"] = 1
        else:
            # First time
            self.streak_data["current_streak"] = 1

        # Update best streak if current is higher
        if self.streak_data["current_streak"] > self.streak_data.get("best_streak", 0):
            self.streak_data["best_streak"] = self.streak_data["current_streak"]

        self.streak_data["last_study_date"] = today
        self.streak_data["total_study_days"] = self.streak_data.get("total_study_days", 0) + 1

        self.save_streak_data()
        self.status_label.configure(text="🎉 Great! Keep it up!", text_color="#10B981")
        
        # Update display
        self.update_display()

    def update_display(self):
        """Update labels without destroying widgets"""
        if self.streak_number_label:
            current_streak = self.streak_data.get("current_streak", 0)
            self.streak_number_label.configure(text=str(current_streak))
        
        if self.last_date_label:
            last_date_str = self.streak_data.get("last_study_date", "Never")
            self.last_date_label.configure(text=f"Last study: {last_date_str}")
        
        if self.best_label:
            best_streak = self.streak_data.get("best_streak", 0)
            self.best_label.configure(text=f"Best streak: {best_streak} days")

    def reset_streak(self):
        """Reset the current streak"""
        self.streak_data["current_streak"] = 0
        self.streak_data["last_study_date"] = "Never"
        self.save_streak_data()
        self.status_label.configure(text="Streak reset.", text_color="#EF4444")
        self.update_display()
