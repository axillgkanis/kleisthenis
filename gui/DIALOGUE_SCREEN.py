import tkinter.messagebox as messagebox


class DIALOGUE:
    def displaySuccess(self, message):
        messagebox.showinfo("Success", message)

    def displayFail(self, message):
        messagebox.showerror("Error", message)
