import tkinter as tk

class CmdWidget(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):

        self.input = tk.Entry(self)
        self.input.pack(fill=tk.X)
        self.input.bind("<Return>", self.evaluate)

    def evaluate(self, event=None):
        code = self.input.get()
        self.input.delete(0, tk.END)

        print(f">>> {code}")
        try:
            exec(code,globals())
        except Exception as e:
            printe(f"{e}")
            raise(e)

root = tk.Tk()
cmdw = CmdWidget(root)
cmdw.pack(fill=tk.BOTH, expand=True)
