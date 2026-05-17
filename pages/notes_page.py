import customtkinter as ctk
import json
import os
import tkinter as tk
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES_FILE = os.path.join(BASE_DIR, "data", "notes.json")
OLD_NOTES_FILE = os.path.join(BASE_DIR, "data", "notes.txt")

class NotesPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0A0E27")

        main_card = ctk.CTkFrame(self, fg_color="#1A1F3A", corner_radius=20)
        main_card.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            main_card,
            text="My Notes",
            font=("Segoe UI", 20, "bold"),
            text_color="#A78BFA"
        )
        title_label.pack(pady=15, padx=20, anchor="w")

        notes_frame = ctk.CTkFrame(main_card, fg_color="#1A1F3A")
        notes_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        left_panel = ctk.CTkFrame(notes_frame, fg_color="#1A1F3A")
        left_panel.pack(side="left", fill="y", padx=(0, 15), pady=0)

        list_label = ctk.CTkLabel(
            left_panel,
            text="Saved Notes",
            font=("Segoe UI", 16, "bold"),
            text_color="#E0E7FF"
        )
        list_label.pack(pady=(10, 5))

        self.notes_listbox = tk.Listbox(
            left_panel,
            width=28,
            height=18,
            bg="#2D3250",
            fg="#E0E7FF",
            selectbackground="#A78BFA",
            selectforeground="#0A0E27",
            bd=0,
            highlightthickness=0,
            activestyle="none",
            font=("Segoe UI", 12)
        )
        self.notes_listbox.pack(fill="y", expand=True, pady=(0, 10))
        self.notes_listbox.bind("<<ListboxSelect>>", self.on_note_select)

        note_buttons_frame = ctk.CTkFrame(left_panel, fg_color="#1A1F3A")
        note_buttons_frame.pack(pady=(0, 10), fill="x")

        new_btn = ctk.CTkButton(
            note_buttons_frame,
            text="New Note",
            command=self.new_note,
            fg_color="#3B3F59",
            hover_color="#4F5472",
            corner_radius=10
        )
        new_btn.pack(side="left", expand=True, padx=5)

        refresh_btn = ctk.CTkButton(
            note_buttons_frame,
            text="Refresh",
            command=self.refresh_notes_list,
            fg_color="#3B3F59",
            hover_color="#4F5472",
            corner_radius=10
        )
        refresh_btn.pack(side="left", expand=True, padx=5)

        right_panel = ctk.CTkFrame(notes_frame, fg_color="#1A1F3A")
        right_panel.pack(side="left", fill="both", expand=True)

        title_entry_label = ctk.CTkLabel(
            right_panel,
            text="Note Title",
            font=("Segoe UI", 16, "bold"),
            text_color="#E0E7FF"
        )
        title_entry_label.pack(pady=(10, 5), anchor="w", padx=10)

        self.title_entry = ctk.CTkEntry(
            right_panel,
            placeholder_text="Enter note title",
            fg_color="#2D3250",
            text_color="#E0E7FF",
            border_color="#A78BFA",
            border_width=2,
            corner_radius=10,
            width=400
        )
        self.title_entry.pack(fill="x", padx=10, pady=(0, 10))

        self.text_editor = ctk.CTkTextbox(
            right_panel,
            fg_color="#2D3250",
            text_color="#E0E7FF",
            border_color="#A78BFA",
            border_width=2,
            corner_radius=10,
            font=("Segoe UI", 13)
        )
        self.text_editor.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = ctk.CTkFrame(right_panel, fg_color="#1A1F3A")
        btn_frame.pack(fill="x", padx=10, pady=(0, 20))

        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save Note",
            font=("Segoe UI", 13, "bold"),
            fg_color="#A78BFA",
            hover_color="#9370DB",
            command=self.save_note,
            corner_radius=10
        )
        save_btn.pack(side="left", padx=10)

        clear_btn = ctk.CTkButton(
            btn_frame,
            text="Clear",
            font=("Segoe UI", 13, "bold"),
            fg_color="#2D3250",
            hover_color="#3D4560",
            command=self.new_note,
            corner_radius=10
        )
        clear_btn.pack(side="left", padx=10)

        delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete",
            font=("Segoe UI", 13, "bold"),
            fg_color="#933D72",
            hover_color="#B05091",
            command=self.delete_note,
            corner_radius=10
        )
        delete_btn.pack(side="left", padx=10)

        self.note_status_label = ctk.CTkLabel(
            right_panel,
            text="",
            font=("Segoe UI", 14),
            text_color="#A78BFA"
        )
        self.note_status_label.pack(pady=(0, 10), anchor="w", padx=10)

        self.current_note_id = None
        self.notes = []
        self.refresh_notes_list()

    def load_storage(self):
        os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
        if not os.path.exists(NOTES_FILE) and os.path.exists(OLD_NOTES_FILE):
            try:
                with open(OLD_NOTES_FILE, "r", encoding="utf-8") as old_file:
                    content = old_file.read()
                data = {"notes": [{"id": str(uuid.uuid4()), "title": "Saved Note", "content": content}]}
                with open(NOTES_FILE, "w", encoding="utf-8") as new_file:
                    json.dump(data, new_file, indent=2)
                return data
            except Exception:
                return {"notes": []}

        if os.path.exists(NOTES_FILE):
            try:
                with open(NOTES_FILE, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception:
                return {"notes": []}

        return {"notes": []}

    def save_storage(self):
        os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
        with open(NOTES_FILE, "w", encoding="utf-8") as file:
            json.dump({"notes": self.notes}, file, indent=2)

    def refresh_notes_list(self):
        data = self.load_storage()
        self.notes = data.get("notes", [])
        self.notes_listbox.delete(0, tk.END)
        for note in self.notes:
            self.notes_listbox.insert(tk.END, note.get("title", "Untitled"))

        if self.current_note_id:
            for index, note in enumerate(self.notes):
                if note.get("id") == self.current_note_id:
                    self.notes_listbox.selection_set(index)
                    break
        self.note_status_label.configure(text=f"{len(self.notes)} saved note(s).")

    def get_selected_note_index(self):
        selection = self.notes_listbox.curselection()
        if not selection:
            return None
        return selection[0]

    def on_note_select(self, event=None):
        index = self.get_selected_note_index()
        if index is None:
            return
        note = self.notes[index]
        self.current_note_id = note.get("id")
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note.get("title", ""))
        self.text_editor.delete("1.0", "end")
        self.text_editor.insert("1.0", note.get("content", ""))

    def save_note(self):
        title = self.title_entry.get().strip() or "Untitled"
        content = self.text_editor.get("1.0", "end-1c")
        if self.current_note_id:
            for note in self.notes:
                if note.get("id") == self.current_note_id:
                    note["title"] = title
                    note["content"] = content
                    break
        else:
            self.current_note_id = str(uuid.uuid4())
            self.notes.append({"id": self.current_note_id, "title": title, "content": content})

        self.save_storage()
        self.refresh_notes_list()
        if self.current_note_id:
            for index, note in enumerate(self.notes):
                if note.get("id") == self.current_note_id:
                    self.notes_listbox.selection_clear(0, tk.END)
                    self.notes_listbox.selection_set(index)
                    self.notes_listbox.see(index)
                    break
        self.note_status_label.configure(text="Note saved.")

    def new_note(self):
        self.current_note_id = None
        self.title_entry.delete(0, tk.END)
        self.text_editor.delete("1.0", "end")
        self.notes_listbox.selection_clear(0, tk.END)
        self.note_status_label.configure(text="New note ready.")

    def delete_note(self):
        index = self.get_selected_note_index()
        if index is None:
            return
        note = self.notes.pop(index)
        if note.get("id") == self.current_note_id:
            self.new_note()
        self.save_storage()
        self.refresh_notes_list()
        self.note_status_label.configure(text="Note deleted.")
