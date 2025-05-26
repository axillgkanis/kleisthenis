import customtkinter as ctk
from dialog_screens.propose_frame import ProposeFramePopup
from dialog_screens.frame_viewer import FrameViewerPopup
import json
import os

DATA_FILE = "proposed_frames.json"

class FramesView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.all_frames = []
        self.search_var = ctk.StringVar()
        self.filter_voted = ctk.StringVar(value="Όλα")
        self.filter_status = ctk.StringVar(value="Όλα")

        self.search_var.trace("w", lambda *args: self.render_frame_list())
        self.filter_voted.trace("w", lambda *args: self.render_frame_list())
        self.filter_status.trace("w", lambda *args: self.render_frame_list())

        ctk.CTkLabel(self, text="Πλαίσια", font=("Arial", 20, "bold")).pack(pady=(10, 5))

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(pady=(0, 10), fill="x", padx=20)

        ctk.CTkLabel(search_frame, text="Αναζήτηση:", font=("Arial", 12)).pack(side="left", padx=5)
        ctk.CTkEntry(search_frame, textvariable=self.search_var, width=200, placeholder_text="Filter by title").pack(side="left")

        ctk.CTkLabel(search_frame, text="\tΨήφος:", font=("Arial", 12)).pack(side="left", padx=5)
        ctk.CTkOptionMenu(search_frame, variable=self.filter_voted, values=["Όλα", "Ψηφισμένα", "Μη ψηφισμένα"]).pack(side="left")

        ctk.CTkLabel(search_frame, text="\tΚατάσταση:", font=("Arial", 12)).pack(side="left", padx=5)
        ctk.CTkOptionMenu(search_frame, variable=self.filter_status, values=["Όλα", "Ενεργά", "Ανενεργά"]).pack(side="left")

        self.list_container = ctk.CTkFrame(self, fg_color="transparent")
        self.list_container.pack(pady=10, fill="both", expand=True)

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(pady=10)

        ctk.CTkButton(btns, text="Πρόταση Πλαισίου", command=self.open_propose_popup).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="Προβολή Προτεινόμενων Πλαισίων", command=self.open_popup_view).pack(side="left", padx=10)

        self.load_frames()
        self.render_frame_list()

    def open_propose_popup(self):
        popup = ProposeFramePopup(self)
        self.wait_window(popup)
        self.load_frames()
        self.render_frame_list()

    def open_popup_view(self):
        from dialog_screens.view_proposed import ViewProposedFramesPopup
        ViewProposedFramesPopup(self)

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
        voted_filter = self.filter_voted.get()
        status_filter = self.filter_status.get()
        user_email = "demo@example.com"

        def frame_matches(frame):
            if keyword and keyword not in frame.get("title", "").lower():
                return False

            if voted_filter == "Ψηφισμένα" and user_email not in frame.get("voted_by", []):
                return False
            elif voted_filter == "Μη ψηφισμένα" and user_email in frame.get("voted_by", []):
                return False

            status = frame.get("status", "pending")
            if status_filter == "Ενεργά" and status != "pending":
                return False
            elif status_filter == "Ανενεργά" and status == "pending":
                return False

            return True

        filtered = [f for f in self.all_frames if frame_matches(f)]

        if not filtered:
            ctk.CTkLabel(self.list_container, text="Δεν βρέθηκαν πλαίσια.", text_color="gray").pack(pady=10)
            return

        for frame in filtered:
            title = frame.get("title", "Untitled")

            def make_open_callback(frame=frame):
                return lambda: FrameViewerPopup(self, frame)

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
