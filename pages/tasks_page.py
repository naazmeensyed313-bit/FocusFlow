import customtkinter as ctk
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASKS_FILE = os.path.join(BASE_DIR, "data", "tasks.json")

class TasksPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#0A0E27")

        self.tasks = []

        main_card = ctk.CTkFrame(self, fg_color="#1A1F3A", corner_radius=20)
        main_card.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            main_card,
            text="Today's Tasks ✅",
            font=("Segoe UI", 34, "bold"),
            text_color="#A78BFA"
        )
        title.pack(pady=20, anchor="w", padx=20)

        input_frame = ctk.CTkFrame(main_card, fg_color="#1A1F3A")
        input_frame.pack(pady=10, padx=20, fill="x")

        self.task_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter task...",
            width=400,
            height=40,
            fg_color="#2D3250",
            text_color="#E0E7FF",
            border_color="#A78BFA",
            border_width=2
        )
        self.task_entry.pack(side="left", padx=10, pady=10)

        add_btn = ctk.CTkButton(
            input_frame,
            text="Add Task",
            width=140,
            height=40,
            command=self.add_task,
            fg_color="#A78BFA",
            hover_color="#9370DB"
        )
        add_btn.pack(side="left", padx=10, pady=10)

        self.status_label = ctk.CTkLabel(
            main_card,
            text="",
            font=("Segoe UI", 14),
            text_color="#A78BFA"
        )
        self.status_label.pack(pady=(5, 10), padx=20, anchor="w")

        self.tasks_frame = ctk.CTkScrollableFrame(
            main_card,
            fg_color="#1A1F3A",
            width=700,
            height=400,
            corner_radius=20
        )
        self.tasks_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.load_tasks()

    # ================= ADD TASK =================
    def add_task(self):

        task_text = self.task_entry.get()

        if task_text.strip() == "":
            self.status_label.configure(text="Please enter a task before saving.")
            return

        self.tasks.append(task_text)
        self.save_tasks()
        self.display_tasks()
        self.task_entry.delete(0, "end")
        self.status_label.configure(text="Task added.")

    # ================= DISPLAY TASKS =================
    def display_tasks(self):

        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        if not self.tasks:
            empty_label = ctk.CTkLabel(
                self.tasks_frame,
                text="No tasks yet. Add one above.",
                font=("Arial", 18),
                text_color="#A78BFA"
            )
            empty_label.pack(pady=20)
            return

        for task in self.tasks:

            task_row = ctk.CTkFrame(self.tasks_frame)
            task_row.pack(fill="x", pady=5, padx=5)

            task_label = ctk.CTkLabel(
                task_row,
                text=task,
                font=("Arial", 18)
            )
            task_label.pack(side="left", padx=10, pady=10)

            delete_btn = ctk.CTkButton(
                task_row,
                text="Delete",
                width=80,
                command=lambda t=task: self.delete_task(t)
            )
            delete_btn.pack(side="right", padx=10)

    # ================= DELETE TASK =================
    def delete_task(self, task):

        self.tasks.remove(task)
        self.save_tasks()
        self.display_tasks()
        self.status_label.configure(text="Task deleted.")

    # ================= SAVE TASKS =================
    def save_tasks(self):

        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)

        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(self.tasks, file)

    # ================= LOAD TASKS =================
    def load_tasks(self):

        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, "r", encoding="utf-8") as file:
                    self.tasks = json.load(file)
            except json.JSONDecodeError:
                self.tasks = []

        self.display_tasks()