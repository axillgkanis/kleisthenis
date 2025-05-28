import customtkinter as ctk
import os
from dialog_screens.frameManager import frameManager
from dialog_screens.DIALOGUE_SCREEN import DIALOGUE_SCREEN

class FRAMEWORK_SCREEN(ctk.CTkToplevel):
    def __init__(self, parent, frame_data, user_email="demo@example.com"):
        super().__init__(parent)
        self.title("Προβολή Πλαισίου")
        self.geometry("400x400")
        self.configure(fg_color="#0f172a")

        self.frame_data = frame_data
        self.user_email = user_email
        self.frame_manager = frameManager()

        title = frame_data.get("title", "Untitled")
        body = frame_data.get("body", "")
        voted = frame_data.get("vote", 0) == 1
        
        # Title
        ctk.CTkLabel(self, text=title, font=("Arial", 16, "bold"), text_color="#e2e8f0").pack(pady=(10, 5))
        
        # Content
        ctk.CTkLabel(self, text=body, wraplength=350, font=("Arial", 12), text_color="#e2e8f0").pack(pady=(5, 10))
        
        # If already voted
        if voted:
            ctk.CTkButton(self, text="Ψηφισμένο", fg_color="#10b981", state="disabled").pack(pady=10)
            ctk.CTkLabel(self, text="Αυτό το πλαίσιο έχει ήδη ψηφιστεί.", text_color="orange").pack(pady=5)
            return

        # Vote buttons
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(pady=10)

        ctk.CTkButton(btns, text="ΥΠΕΡ", fg_color="#10b981", command=lambda: self.cast_vote("agree")).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="ΚΑΤΑ", fg_color="#ef4444", command=lambda: self.cast_vote("disagree")).pack(side="left", padx=10)

    def cast_vote(self, vote_type):
        try:
            # Get framework ID from the data
            framework_id = self.frame_data.get("id")
            
            if not framework_id:
                ctk.CTkLabel(self, text="Σφάλμα: Δεν βρέθηκε αναγνωριστικό πλαισίου.", text_color="red").pack(pady=10)
                return
                
            # Use frameManager to create vote and update framework status
            result = self.frame_manager.createVote(
                framework_id=framework_id,
                vote_choice=vote_type,
                voter_id=self.user_email
            )
            
            if result:
                DIALOGUE_SCREEN().displaySuccess("Η ψήφος σας καταγράφηκε επιτυχώς!")
                self.destroy()
            else:
                ctk.CTkLabel(self, text="Σφάλμα κατά την καταγραφή της ψήφου.", text_color="red").pack(pady=10)
                
        except Exception as e:
            ctk.CTkLabel(self, text=f"Σφάλμα: {e}", text_color="red").pack(pady=10)