import tkinter.messagebox as messagebox

class DIALOGUE_SCREEN:
    def displaySuccess(self, message):
        messagebox.showinfo("Success", message)

    def displayFail(self, message):
         messagebox.showerror("Error", message)
