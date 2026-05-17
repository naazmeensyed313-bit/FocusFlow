import customtkinter as ctk
import json
import os

from pages.dashboard import DashboardPage
from pages.timer_page import TimerPage
from pages.notes_page import NotesPage
from pages.tasks_page import TasksPage
from pages.streak_page import StreakPage

ctk.set_appearance_mode("dark")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")
        self.title("Virtual Study Room - Modern Dashboard")
        
        # Navy blue background
        self.configure(fg_color="#0A0E27")
        
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="#0A0E27")
        main_container.pack(fill="both", expand=True)
        
        # ==================== SIDEBAR ====================
        sidebar = ctk.CTkFrame(main_container, fg_color="#1A1F3A", corner_radius=0, width=300)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo
        logo_frame = ctk.CTkFrame(sidebar, fg_color="#1A1F3A")
        logo_frame.pack(pady=30, padx=20, fill="x")
        
        logo = ctk.CTkLabel(
            logo_frame,
            text="📚 Virtual Study Room",
            font=("Segoe UI", 20, "bold"),
            text_color="#B0B3B3",
            wraplength=240,
            justify="center"
        )
        logo.pack()
        
        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", "🏠", "dashboard_page"),
            ("Timer", "⏰", "timer_page"),
            ("Tasks", "📋", "tasks_page"),
            ("Notes", "📝", "notes_page"),
            ("Streak", "🔥", "streak_page"),
        ]
        
        for label, icon, page_id in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=f"{icon} {label}",
                font=("Segoe UI", 14, "bold"),
                height=50,
                fg_color="#2D3250",
                hover_color="#A78BFA",
                text_color="#E0E7FF",
                command=lambda pid=page_id: self.show_page(pid),
                border_width=0,
                corner_radius=12
            )
            btn.pack(pady=10, padx=15, fill="x")
            self.nav_buttons[page_id] = (btn, label)
        
        # ==================== MAIN CONTENT ====================
        content_frame = ctk.CTkFrame(main_container, fg_color="#0A0E27")
        content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Title bar
        title_frame = ctk.CTkFrame(content_frame, fg_color="#0A0E27")
        title_frame.pack(fill="x", pady=(0, 20))
        
        self.page_title = ctk.CTkLabel(
            title_frame,
            text="Dashboard",
            font=("Segoe UI", 32, "bold"),
            text_color="#E0E7FF"
        )
        self.page_title.pack(anchor="w")
        
        # Pages container
        self.pages_container = ctk.CTkFrame(content_frame, fg_color="#0A0E27")
        self.pages_container.pack(fill="both", expand=True)
        
        self.pages = {}
        for PageClass, page_id in [
            (DashboardPage, "dashboard_page"),
            (TimerPage, "timer_page"),
            (NotesPage, "notes_page"),
            (TasksPage, "tasks_page"),
            (StreakPage, "streak_page"),
        ]:
            page = PageClass(self.pages_container)
            self.pages[page_id] = page
            page.place(relwidth=1, relheight=1)
        
        self.current_page = "dashboard_page"
        self.show_page("dashboard_page")
    
    def show_page(self, page_id):
        self.current_page = page_id
        for pid, page in self.pages.items():
            if pid == page_id:
                page.tkraise()
                # Update title
                label = self.nav_buttons[page_id][1]
                self.page_title.configure(text=label)
            else:
                page.lower()

if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()
