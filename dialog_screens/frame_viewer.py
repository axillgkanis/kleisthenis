import customtkinter as ctk
import os
import json

class FrameViewerPopup(ctk.CTkToplevel):
    def __init__(self, parent, frame_data, user_email="demo@example.com"):
        super().__init__(parent)
        self.title("View Frame")
        self.geometry("400x400")
        self.configure(fg_color="#0f172a")

        self.frame_data = frame_data
        self.user_email = user_email  # Θα γίνει δυναμικό αργότερα

        title = frame_data.get("title", "Untitled")
        description = frame_data.get("description", "")
        pdf = frame_data.get("pdf_file", None)
        voted_by = frame_data.get("voted_by", [])
        votes = frame_data.get("votes", {"agree": 0, "disagree": 0})

        # --- UI Elements
        ctk.CTkLabel(self, text="LOGO", font=("Arial", 18, "bold"), text_color="white").pack(pady=(10, 5))
        ctk.CTkLabel(self, text=title, font=("Arial", 14, "bold"), text_color="white").pack(pady=(5, 5))

        content = f"📄 {os.path.basename(pdf)}" if pdf else description
        ctk.CTkLabel(self, text=content, wraplength=350, font=("Arial", 12), text_color="#e2e8f0").pack(pady=(5, 10))

        # --- Αν έχει ήδη ψηφίσει
        if self.user_email in voted_by:
            btns = ctk.CTkFrame(self, fg_color="transparent")
            btns.pack(pady=10)

            # Guess από balance (εφόσον δεν έχουμε per-user vote value)
            voted_text = "AGREE" if votes.get("agree", 0) >= votes.get("disagree", 0) else "DISAGREE"
            color = "#10b981" if voted_text == "AGREE" else "#ef4444"

            ctk.CTkButton(btns, text=voted_text, fg_color=color, state="disabled").pack(padx=10, pady=10)
            ctk.CTkLabel(self, text="Έχετε ήδη ψηφίσει για αυτό το πλαίσιο.", text_color="orange").pack(pady=5)
            return

        # --- Αν δεν έχει ψηφίσει ακόμα
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(pady=10)

        ctk.CTkButton(btns, text="AGREE", fg_color="#10b981", command=lambda: self.cast_vote("agree")).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="DISAGREE", fg_color="#ef4444", command=lambda: self.cast_vote("disagree")).pack(side="left", padx=10)

    def cast_vote(self, vote_type):
        try:
            with open("proposed_frames.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            for f in data:
                if (
                    f["title"] == self.frame_data["title"]
                    and f.get("pdf_file") == self.frame_data.get("pdf_file")
                ):
                    # Αρχικοποίηση votes/voted_by αν δεν υπάρχουν
                    f.setdefault("votes", {"agree": 0, "disagree": 0})
                    f.setdefault("voted_by", [])

                    # Αν έχει ήδη ψηφίσει (safety check)
                    if self.user_email in f["voted_by"]:
                        break

                    f["votes"][vote_type] += 1
                    f["voted_by"].append(self.user_email)
                    break

            with open("proposed_frames.json", "w", encoding="utf-8") as f_out:
                json.dump(data, f_out, indent=4)

            self.destroy()

        except Exception as e:
            ctk.CTkLabel(self, text=f"Σφάλμα: {e}", text_color="red").pack(pady=10)