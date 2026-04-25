import tkinter as tk
from tkinter import ttk

def app():
    window = tk.Tk()
    window.title("Database Application")
    window.geometry("1000x600")

    frame = ttk.Frame(window, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    heading = ttk.Label(frame, text="Northshore LogisticsDatabase Application", font=("Helvetica", 16))
    heading.pack(pady=10)

    message = ttk.Label(frame, text="Welcome to the Northshore Logistics Database Application!")
    message.pack(pady=10)

    window.mainloop()