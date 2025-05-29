import customtkinter as ctk
from dialog_screens.FRAME_PROPOSAL_SCREEN import FRAME_PROPOSAL_SCREEN
from dialog_screens.FRAMEWORK_SCREEN import FRAMEWORK_SCREEN
import json
import os

DATA_FILE = "proposed_frames.json"


class FramesView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.all_frames = []  # Αποθηκεύει όλα τα frames από το αρχείο
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self.render_frame_list())

        # Τίτλος
        ctk.CTkLabel(self, text="Πλαίσια", font=(
            "Arial", 20, "bold")).pack(pady=(10, 5))

        # Search / Filtering Entry
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(pady=(0, 10), fill="x", padx=20)

        ctk.CTkLabel(search_frame, text="Search:", font=(
            "Arial", 12)).pack(side="left", padx=5)
        ctk.CTkEntry(search_frame, textvariable=self.search_var, width=300,
                     placeholder_text="Filter by title...").pack(side="left")

        # Frame List container
        self.list_container = ctk.CTkFrame(self, fg_color="transparent")
        self.list_container.pack(pady=10, fill="both", expand=True)

        # Κουμπιά Propose / View
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(pady=10)

        self.load_frames()
        self.render_frame_list()

    def load_frames(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.all_frames = json.load(f)
        else:
            self.all_frames = []

    def render_frame_list(self):
        for widget in self.list_container.winfo_children():
            widget.destroy()

        keyword = self.search_var.get().lower()

        filtered = [
            f for f in self.all_frames
            if keyword in f.get("title", "").lower()
        ]

        if not filtered:
            ctk.CTkLabel(self.list_container, text="No frames found.",
                         text_color="gray").pack(pady=10)
            return

        for frame in filtered:
            title = frame.get("title", "Untitled")

            def make_open_callback(frame=frame):
                return lambda: FRAMEWORK_SCREEN(self, frame)

            btn = ctk.CTkButton(
                self.list_container,
                text=title,
                anchor="w",
                fg_color="#1e293b",
                hover_color="#334155",
                font=("Arial", 13),
                command=make_open_callback()
            )
            btn.pack(fill="x", padx=30, pady=5)
