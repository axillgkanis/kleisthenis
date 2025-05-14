import tkinter as tk
from tkinter import filedialog, messagebox
import json, os

# Colors
BG_COLOR = "#f9fafb"
SIDEBAR_COLOR = "#e0e7ff"
CONTENT_BG = "#ffffff"
TEXT_COLOR = "#0f172a"
BUTTON_BG = "#93c5fd"
BUTTON_FG = "#0f172a"
BUTTON_HOVER = "#60a5fa"
PINK_TAG = "#fce7f3"
DATA_FILE = "proposed_frames.json"

root = tk.Tk()
root.title("Kleisthenis Dashboard")
root.geometry("1000x700")
root.configure(bg=BG_COLOR)

# Sidebar
sidebar = tk.Frame(root, bg=SIDEBAR_COLOR, width=200)
sidebar.pack(side="left", fill="y")

content = tk.Frame(root, bg=CONTENT_BG)
content.pack(side="right", expand=True, fill="both")

# Sidebar buttons
def clear_content():
    for widget in content.winfo_children():
        widget.destroy()

selected_pdf_path = tk.StringVar()
current_edit_index = None

# Propose Frame View

def show_propose_view(frame_data=None, index=None):
    global current_edit_index
    clear_content()
    current_edit_index = index

    tk.Label(content, text="Propose New Frame" if frame_data is None else "Edit Frame",
             font=("Helvetica", 20, "bold"), bg=CONTENT_BG, fg=TEXT_COLOR).pack(pady=20)

    form = tk.Frame(content, bg=PINK_TAG, padx=20, pady=20)
    form.pack(pady=10)

    tk.Label(form, text="Frame Title:", bg=PINK_TAG, font=("Helvetica", 12)).pack(anchor="w")
    title_entry = tk.Entry(form, width=50, font=("Helvetica", 11))
    title_entry.pack(pady=5)

    tk.Label(form, text="Description:", bg=PINK_TAG, font=("Helvetica", 12)).pack(anchor="w")
    desc_text = tk.Text(form, height=6, width=50, font=("Helvetica", 10))
    desc_text.pack(pady=5)

    selected_file_label = tk.Label(form, text="No file selected", bg=PINK_TAG,
                                   font=("Helvetica", 10), fg="#6b7280")
    selected_file_label.pack(pady=5)

    if frame_data:
        title_entry.insert(0, frame_data.get("title", ""))
        desc_text.insert("1.0", frame_data.get("description", ""))
        if frame_data.get("pdf_file"):
            selected_pdf_path.set(frame_data["pdf_file"])
            selected_file_label.config(text=f"📎 {os.path.basename(frame_data['pdf_file'])}")

    def select_pdf():
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            selected_pdf_path.set(file_path)
            selected_file_label.config(text=f"📎 {os.path.basename(file_path)}")

    def submit_frame():
        title = title_entry.get().strip()
        desc = desc_text.get("1.0", tk.END).strip()
        pdf = selected_pdf_path.get()

        if not title:
            messagebox.showwarning("Missing Title", "Please enter a title for the frame.")
            return

        new_frame = {"title": title, "description": desc, "pdf_file": pdf or None}

        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        if current_edit_index is not None:
            data[current_edit_index] = new_frame
        else:
            data.append(new_frame)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        title_entry.delete(0, tk.END)
        desc_text.delete("1.0", tk.END)
        selected_file_label.config(text="No file selected")
        selected_pdf_path.set("")

        messagebox.showinfo("Success", "Frame saved successfully!")
        show_view_frames()

    tk.Button(form, text="📎 Select PDF", command=select_pdf,
              bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica", 11, "bold")).pack(pady=5)

    btns = tk.Frame(form, bg=PINK_TAG)
    btns.pack(pady=10)
    tk.Button(btns, text="Update" if frame_data else "Submit", command=submit_frame,
              bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica", 11, "bold"), padx=10).pack(side="left", padx=5)
    tk.Button(btns, text="Cancel", command=clear_content,
              bg="#f87171", fg="white", font=("Helvetica", 11), padx=10).pack(side="left", padx=5)

# View Frames View

def show_view_frames():
    clear_content()

    tk.Label(content, text="Submitted Frames", font=("Helvetica", 20, "bold"),
             bg=CONTENT_BG, fg=TEXT_COLOR).pack(pady=20)

    if not os.path.exists(DATA_FILE):
        tk.Label(content, text="No frames submitted yet.", font=("Helvetica", 12),
                 bg=CONTENT_BG, fg="#6b7280").pack(pady=10)
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        tk.Label(content, text="No frames submitted yet.", font=("Helvetica", 12),
                 bg=CONTENT_BG, fg="#6b7280").pack(pady=10)
        return

    for i, frame in enumerate(data):
        card = tk.Frame(content, bg="#f1f5f9", bd=1, relief="solid", padx=15, pady=10)
        card.pack(fill="x", padx=30, pady=10)

        tk.Label(card, text=frame.get("title", "No Title"), font=("Helvetica", 14, "bold"),
                 bg="#f1f5f9", fg=TEXT_COLOR).pack(anchor="w")
        tk.Label(card, text=frame.get("description", "No Description"), wraplength=800,
                 justify="left", bg="#f1f5f9", fg=TEXT_COLOR).pack(anchor="w", pady=(5, 0))

        if frame.get("pdf_file"):
            tk.Label(card, text=f" Attached File: {os.path.basename(frame['pdf_file'])}",
                     font=("Helvetica", 10), bg="#f1f5f9", fg="#475569").pack(anchor="w", pady=(5, 0))

        actions = tk.Frame(card, bg="#f1f5f9")
        actions.pack(anchor="e", pady=(10, 0))

        def make_delete_callback(index=i):
            def delete():
                confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this frame?")
                if confirm:
                    del data[index]
                    with open(DATA_FILE, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
                    show_view_frames()
            return delete

        tk.Button(actions, text="Delete", command=make_delete_callback(i),
                  bg="#f87171", fg="black", font=("Helvetica", 10)).pack(side="right", padx=5)
        tk.Button(actions, text="Edit", command=lambda idx=i: show_propose_view(data[idx], idx),
                  bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica", 10)).pack(side="right", padx=5)

# Sidebar buttons
tk.Label(sidebar, text="Menu", font=("Helvetica", 16, "bold"), bg=SIDEBAR_COLOR).pack(pady=20)
tk.Button(sidebar, text="Propose Frame", command=lambda: show_propose_view(),
          bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica", 12), width=18).pack(pady=5)
tk.Button(sidebar, text="View Frames", command=show_view_frames,
          bg=BUTTON_BG, fg=BUTTON_FG, font=("Helvetica", 12), width=18).pack(pady=5)
tk.Button(sidebar, text="Exit", command=root.destroy,
          bg="#e5e7eb", fg="black", font=("Helvetica", 12), width=18).pack(pady=5)

root.mainloop()