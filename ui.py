import tkinter as tk
import tkinter.ttk as ttk
from db import add_shipment
from db import add_delivery
from db import add_incident


def app():
    window = tk.Tk()
    window.title("Database Application")
    window.geometry("1000x600")

    left_frame = tk.Frame(window, bg="#003a6b")
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    right_frame = tk.Frame(window, bg="#003a6b")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    menu_area = tk.Frame(left_frame, width=250, bg="#3776a1")
    menu_area.pack(fill=tk.Y, expand=True, padx=5, pady=5)
    menu_area.pack_propagate(False)

    content_area = tk.Frame(right_frame, bg="#5293bb")
    content_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def clear_content():
        for widget in content_area.winfo_children():
            widget.destroy()

    def home():
        clear_content()
        home_label = tk.Label(content_area, text="Welcome to the Northshore Logistics Database Application", bg="#89cff1", fg="#003a6b", font=("Courier New", 16), padx=20, pady=20)
        home_label.pack(pady=20, padx=20, anchor="nw")

    def show_shipments():
        clear_content()

        title = tk.Label(content_area, text="Add Shipment", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
        title.pack(pady=20, padx=20, anchor="nw")

        form = tk.Frame(content_area, bg="#5293bb")
        form.pack(pady=10, padx=20, anchor="nw")

        tk.Label(form, text="Order Number:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        order_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        order_entry.pack(pady=5)

        tk.Label(form, text="Sender Details:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        sender_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        sender_entry.pack(pady=5)

        tk.Label(form, text="Receiver Details:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        receiver_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        receiver_entry.pack(pady=5)

        tk.Label(form, text="Item Description:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        item_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        item_entry.pack(pady=5)

        tk.Label(form, text="Transport Cost:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        transport_cost_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        transport_cost_entry.pack(pady=5)

        tk.Label(form, text="Surcharge:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        surcharge_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        surcharge_entry.pack(pady=5)

        tk.Label(form, text="Payment Status:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        payment_status_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        payment_status_entry.pack(pady=5)

        tk.Label(form, text="Delivery Status:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        delivery_status_entry = ttk.Combobox(form, values=["Select Delivery Status", "Dispatched", "On the way", "Delivered", "Delayed", "Returned"], font=("Courier New", 12), width=47, state="readonly")
        delivery_status_entry.pack(pady=5)
        delivery_status_entry.current(0)

        def submit():
            add_shipment(order_entry.get(), sender_entry.get(), receiver_entry.get(), item_entry.get(), delivery_status_entry.get(), transport_cost_entry.get(), surcharge_entry.get(), payment_status_entry.get())

            title.config(text="Shipment added")

            order_entry.delete(0, tk.END)
            sender_entry.delete(0, tk.END)
            receiver_entry.delete(0, tk.END)
            item_entry.delete(0, tk.END)
            transport_cost_entry.delete(0, tk.END)
            surcharge_entry.delete(0, tk.END)
            payment_status_entry.delete(0, tk.END)
            delivery_status_entry.set("Select Delivery Status")

            window.after(1000, lambda: title.config(text="Add Shipment"))

        tk.Button(form, text="Add Shipment", command=submit, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=15)

    def show_deliveries():
        clear_content()

        title = tk.Label(content_area, text="Add Delivery", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
        title.pack(pady=20, padx=20, anchor="nw")

        form = tk.Frame(content_area, bg="#5293bb")
        form.pack(pady=10, padx=20, anchor="nw")

        tk.Label(form, text="Shipment ID:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        shipment_id_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        shipment_id_entry.pack(pady=5)

        tk.Label(form, text="Delivery Date:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        delivery_date_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        delivery_date_entry.pack(pady=5)

        tk.Label(form, text="Assigned Driver:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        assigned_driver_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        assigned_driver_entry.pack(pady=5)

        tk.Label(form, text="Route Details:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        route_details_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        route_details_entry.pack(pady=5)

        def submit_delivery():
            add_delivery(shipment_id_entry.get(), delivery_date_entry.get(), assigned_driver_entry.get(), route_details_entry.get())

            title.config(text="Delivery added")

            shipment_id_entry.delete(0, tk.END)
            delivery_date_entry.delete(0, tk.END)
            assigned_driver_entry.delete(0, tk.END)
            route_details_entry.delete(0, tk.END)

            window.after(1000, lambda: title.config(text="Add Delivery"))

        tk.Button(form, text="Add Delivery", command=submit_delivery, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=15)

    def show_incidents():
        clear_content()

        title = tk.Label(content_area, text="Add Incident", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
        title.pack(pady=20, padx=20, anchor="nw")

        form = tk.Frame(content_area, bg="#5293bb")
        form.pack(pady=10, padx=20, anchor="nw")

        tk.Label(form, text="Shipment ID:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        shipment_id_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        shipment_id_entry.pack(pady=5)

        tk.Label(form, text="Incident Type:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        incident_type_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        incident_type_entry.pack(pady=5)

        tk.Label(form, text="Incident Description:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        incident_description_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        incident_description_entry.pack(pady=5)

        def submit_incident():
            add_incident(shipment_id_entry.get(), incident_type_entry.get(), incident_description_entry.get())

            title.config(text="Incident added")

            shipment_id_entry.delete(0, tk.END)
            incident_type_entry.delete(0, tk.END)
            incident_description_entry.delete(0, tk.END)

            window.after(1000, lambda: title.config(text="Add Incident"))

        tk.Button(form, text="Add Incident", command=submit_incident, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=15)

    tk.Button(menu_area, text="Home", command=home, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2).pack(pady=20, padx=20)
    tk.Button(menu_area, text="Shipments", command=show_shipments, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2).pack(pady=20, padx=20)
    tk.Button(menu_area, text="Deliveries", command=show_deliveries, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2).pack(pady=20, padx=20)
    tk.Button(menu_area, text="Incidents", command=show_incidents, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2).pack(pady=20, padx=20)

    def close_app():
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", close_app)

    window.mainloop()