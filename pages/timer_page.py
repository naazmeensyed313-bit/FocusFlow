import customtkinter as ctk

class TimerPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="#0A0E27")

        self.time_left = 0
        self.initial_time = 0
        self.is_running = False

        main_card = ctk.CTkFrame(self, fg_color="#1A1F3A", corner_radius=20)
        main_card.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            main_card,
            text="Timer ⏰",
            font=("Segoe UI", 34, "bold"),
            text_color="#A78BFA"
        )
        title.pack(pady=20, anchor="w", padx=20)

        input_frame = ctk.CTkFrame(main_card, fg_color="#1A1F3A")
        input_frame.pack(pady=10, padx=20)

        self.hours_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="HH",
            width=80,
            justify="center",
            fg_color="#2D3250",
            text_color="#E0E7FF",
            border_color="#A78BFA",
            border_width=2
        )
        self.hours_entry.insert(0, "0")
        self.hours_entry.pack(side="left", padx=5)

        self.minutes_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="MM",
            width=80,
            justify="center",
            fg_color="#2D3250",
            text_color="#E0E7FF",
            border_color="#A78BFA",
            border_width=2
        )
        self.minutes_entry.insert(0, "0")
        self.minutes_entry.pack(side="left", padx=5)

        self.seconds_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="SS",
            width=80,
            justify="center",
            fg_color="#2D3250",
            text_color="#E0E7FF",
            border_color="#A78BFA",
            border_width=2
        )
        self.seconds_entry.insert(0, "0")
        self.seconds_entry.pack(side="left", padx=5)

        labels_frame = ctk.CTkFrame(main_card, fg_color="#1A1F3A")
        labels_frame.pack(pady=(0, 20), padx=20)

        hour_label = ctk.CTkLabel(labels_frame, text="Hours", font=("Segoe UI", 12), text_color="#E0E7FF")
        hour_label.pack(side="left", padx=35)
        minute_label = ctk.CTkLabel(labels_frame, text="Minutes", font=("Segoe UI", 12), text_color="#E0E7FF")
        minute_label.pack(side="left", padx=35)
        second_label = ctk.CTkLabel(labels_frame, text="Seconds", font=("Segoe UI", 12), text_color="#E0E7FF")
        second_label.pack(side="left", padx=35)

        self.timer_label = ctk.CTkLabel(
            main_card,
            text="00:00:00",
            font=("Segoe UI", 72, "bold"),
            text_color="#E0E7FF"
        )
        self.timer_label.pack(pady=20)

        self.status_label = ctk.CTkLabel(
            main_card,
            text="Enter a duration and press Start.",
            font=("Segoe UI", 14),
            text_color="#A78BFA"
        )
        self.status_label.pack(pady=(0, 20), padx=20)

        button_frame = ctk.CTkFrame(main_card, fg_color="#1A1F3A")
        button_frame.pack(pady=10, padx=20, anchor="center")

        start_btn = ctk.CTkButton(
            button_frame,
            text="Start",
            command=self.start_timer,
            fg_color="#A78BFA",
            hover_color="#9370DB"
        )
        start_btn.pack(side="left", padx=10)

        pause_btn = ctk.CTkButton(
            button_frame,
            text="Pause",
            command=self.pause_timer,
            fg_color="#3B3F59",
            hover_color="#4F5472"
        )
        pause_btn.pack(side="left", padx=10)

        reset_btn = ctk.CTkButton(
            button_frame,
            text="Reset",
            command=self.reset_timer,
            fg_color="#3B3F59",
            hover_color="#4F5472"
        )
        reset_btn.pack(side="left", padx=10)

    # ================= UPDATE TIMER =================
    def update_timer_display(self):
        hours = self.time_left // 3600
        minutes = (self.time_left % 3600) // 60
        seconds = self.time_left % 60
        self.timer_label.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def update_timer(self):

        if self.is_running:
            self.update_timer_display()

            if self.time_left > 0:
                self.time_left -= 1
                self.after(1000, self.update_timer)
            else:
                self.timer_label.configure(text="Time's Up!")
                self.is_running = False
                self.status_label.configure(text="Time's Up!")

    def set_time_from_inputs(self):
        try:
            hours = max(0, int(self.hours_entry.get().strip() or 0))
            minutes = max(0, int(self.minutes_entry.get().strip() or 0))
            seconds = max(0, int(self.seconds_entry.get().strip() or 0))
        except ValueError:
            self.status_label.configure(text="Please enter valid numbers for hours, minutes, and seconds.")
            return False

        total_seconds = hours * 3600 + minutes * 60 + seconds
        if total_seconds == 0:
            self.status_label.configure(text="                  Please set a duration before starting.")
            return False

        self.initial_time = total_seconds
        self.time_left = total_seconds
        self.update_timer_display()
        self.status_label.configure(text="Timer set. Press Start.")
        return True

    # ================= START =================
    def start_timer(self):

        if not self.is_running:
            if self.time_left == 0:
                if not self.set_time_from_inputs():
                    return
            self.is_running = True
            self.status_label.configure(text="Timer running...")
            self.update_timer()

    # ================= PAUSE =================
    def pause_timer(self):

        if self.is_running:
            self.is_running = False
            self.status_label.configure(text="Timer paused.")
    # ================= STOP =================
    def stop_timer(self):
        if self.is_running or self.time_left != 0:
            self.is_running = False
            self.time_left = 0
            self.update_timer_display()
            self.status_label.configure(text="Timer stopped.")

    # ================= RESET =================
    def reset_timer(self):

        self.is_running = False
        self.time_left = 0
        self.initial_time = 0

        self.hours_entry.delete(0, "end")
        self.hours_entry.insert(0, "0")
        self.minutes_entry.delete(0, "end")
        self.minutes_entry.insert(0, "0")
        self.seconds_entry.delete(0, "end")
        self.seconds_entry.insert(0, "0")

        self.update_timer_display()
        self.status_label.configure(text="Timer reset.")