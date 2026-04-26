from email.mime import message
import tkinter as tk
from tkinter import ttk
from db import add_shipment

def app():
    window = tk.Tk()
    window.title("Database Application")
    window.geometry("1000x600")

    frame = ttk.Frame(window, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    heading = ttk.Label(frame, text="Northshore Logistics Database Application", font=("Helvetica", 16))
    heading.pack(pady=10)

    message = ttk.Label(frame, text="Welcome to the Northshore Logistics Database Application!")
    message.pack(pady=10)

    ttk.Label(frame, text="Order Number:").pack()
    order_entry = ttk.Entry(frame)
    order_entry.pack()

    ttk.Label(frame, text="Sender Details:").pack()
    sender_entry = ttk.Entry(frame)
    sender_entry.pack()

    ttk.Label(frame, text="Receiver Details:").pack()
    receiver_entry = ttk.Entry(frame)
    receiver_entry.pack()

    ttk.Label(frame, text="Item Description:").pack()
    item_entry = ttk.Entry(frame)
    item_entry.pack()

    def submit():
        add_shipment(order_entry.get(), sender_entry.get(), receiver_entry.get(), item_entry.get())
        message.config(text="Shipment added")
        order_entry.delete(0, tk.END)
        sender_entry.delete(0, tk.END)
        receiver_entry.delete(0, tk.END)
        item_entry.delete(0, tk.END)
        window.after(1000, reset_message)


    def reset_message():
        message.config(text="Ready to add shipment")

    ttk.Button(frame, text="Add Shipment", command=submit).pack(pady=10)


    def close_app():
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", close_app)

    window.mainloop()