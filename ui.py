import tkinter as tk
import tkinter.ttk as ttk
from db import *


def app():
    window = tk.Tk()
    window.title("Database Application")
    window.geometry("1700x900")

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

    def money_check(value):
        try:
            return format(float(value), ".2f")
        except ValueError:
            return None

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
        payment_status_entry = ttk.Combobox(form, values=["Select Payment Status", "Pending", "Fully Paid", "Part Paid", "Not Paid"], font=("Courier New", 12), width=47, state="readonly")
        payment_status_entry.pack(pady=5)
        payment_status_entry.current(0)

        tk.Label(form, text="Delivery Status:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        delivery_status_entry = ttk.Combobox(form, values=["Select Delivery Status", "Dispatched", "On the way", "Delivered", "Delayed", "Returned"], font=("Courier New", 12), width=47, state="readonly")
        delivery_status_entry.pack(pady=5)
        delivery_status_entry.current(0)

        def submit():
            transport_cost = money_check(transport_cost_entry.get())
            surcharge = money_check(surcharge_entry.get())

            if not order_entry.get().isdigit():
                title.config(text="Order number must be numbers only")
                return

            if transport_cost is None:
                title.config(text="Transport cost must be a valid amount")
                return

            if surcharge is None:
                title.config(text="Surcharge must be a valid amount")
                return

            if payment_status_entry.get() == "Select Payment Status":
                title.config(text="Select payment status")
                return

            if delivery_status_entry.get() == "Select Delivery Status":
                title.config(text="Select delivery status")
                return

            add_shipment(order_entry.get(), sender_entry.get(), receiver_entry.get(), item_entry.get(), delivery_status_entry.get(), transport_cost, surcharge, payment_status_entry.get())

            title.config(text="Shipment added")

            order_entry.delete(0, tk.END)
            sender_entry.delete(0, tk.END)
            receiver_entry.delete(0, tk.END)
            item_entry.delete(0, tk.END)
            transport_cost_entry.delete(0, tk.END)
            surcharge_entry.delete(0, tk.END)
            payment_status_entry.current(0)
            delivery_status_entry.current(0)

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
            if not shipment_id_entry.get().isdigit():
                title.config(text="Shipment ID must be numbers only")
                return

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
            if not shipment_id_entry.get().isdigit():
                title.config(text="Shipment ID must be numbers only")
                return

            add_incident(shipment_id_entry.get(), incident_type_entry.get(), incident_description_entry.get())

            title.config(text="Incident added")

            shipment_id_entry.delete(0, tk.END)
            incident_type_entry.delete(0, tk.END)
            incident_description_entry.delete(0, tk.END)

            window.after(1000, lambda: title.config(text="Add Incident"))

        tk.Button(form, text="Add Incident", command=submit_incident, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=15)

    def show_inventory():
        clear_content()

        title = tk.Label(content_area, text="Inventory Management", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
        title.pack(pady=20, padx=20, anchor="nw")

        form = tk.Frame(content_area, bg="#5293bb")
        form.pack(pady=10, padx=20, anchor="nw")

        tk.Label(form, text="Item Name:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        item_name_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        item_name_entry.pack(pady=5)

        tk.Label(form, text="Quantity:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        quantity_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        quantity_entry.pack(pady=5)

        tk.Label(form, text="Reorder Level:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        reorder_level_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        reorder_level_entry.pack(pady=5)

        tk.Label(form, text="Warehouse Location:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        warehouse_location_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        warehouse_location_entry.pack(pady=5)

        def submit_inventory():
            if not quantity_entry.get().isdigit():
                title.config(text="Quantity must be numbers only")
                return

            if not reorder_level_entry.get().isdigit():
                title.config(text="Reorder level must be numbers only")
                return

            add_inventory(item_name_entry.get(), quantity_entry.get(), reorder_level_entry.get(), warehouse_location_entry.get())

            title.config(text="Inventory added")

            item_name_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            reorder_level_entry.delete(0, tk.END)
            warehouse_location_entry.delete(0, tk.END)

            window.after(1000, lambda: title.config(text="Inventory Management"))

        tk.Button(form, text="Add Inventory", command=submit_inventory, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=15)

    def show_vehicles():
        clear_content()

        title = tk.Label(content_area, text="Vehicle Management", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
        title.pack(pady=20, padx=20, anchor="nw")

        form = tk.Frame(content_area, bg="#5293bb")
        form.pack(pady=10, padx=20, anchor="nw")

        tk.Label(form, text="Capacity:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        capacity_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        capacity_entry.pack(pady=5)

        tk.Label(form, text="Maintenance Schedule:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        maintenance_schedule_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        maintenance_schedule_entry.pack(pady=5)

        tk.Label(form, text="Availability:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        availability_entry = ttk.Combobox(form, values=["Select Availability", "Available", "In Use", "Unavailable", "Maintenance"], font=("Courier New", 12), width=47, state="readonly")
        availability_entry.pack(pady=5)
        availability_entry.current(0)

        def submit_vehicle():
            if not capacity_entry.get().isdigit():
                title.config(text="Capacity must be numbers only")
                return

            if availability_entry.get() == "Select Availability":
                title.config(text="Select availability")
                return

            add_vehicle(capacity_entry.get(), maintenance_schedule_entry.get(), availability_entry.get())

            title.config(text="Vehicle added")

            capacity_entry.delete(0, tk.END)
            maintenance_schedule_entry.delete(0, tk.END)
            availability_entry.current(0)

            window.after(1000, lambda: title.config(text="Vehicle Management"))

        tk.Button(form, text="Add Vehicle", command=submit_vehicle, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=15)

    def show_tables():
        clear_content()

        title = tk.Label(content_area, text="Database Tables", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
        title.pack(pady=20, padx=20, anchor="nw")

        notebook = ttk.Notebook(content_area)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        shipments_tab = tk.Frame(notebook, bg="#5293bb")
        deliveries_tab = tk.Frame(notebook, bg="#5293bb")
        incidents_tab = tk.Frame(notebook, bg="#5293bb")
        inventory_tab = tk.Frame(notebook, bg="#5293bb")
        vehicles_tab = tk.Frame(notebook, bg="#5293bb")

        notebook.add(shipments_tab, text="Shipments")
        notebook.add(deliveries_tab, text="Deliveries")
        notebook.add(incidents_tab, text="Incidents")
        notebook.add(inventory_tab, text="Inventory")
        notebook.add(vehicles_tab, text="Vehicles")

        shipment_columns = ("shipment_id", "order_number", "sender_details", "receiver_details", "item_description", "delivery_status", "transport_cost", "surcharge", "payment_status")
        shipment_table = ttk.Treeview(shipments_tab, columns=shipment_columns, show="headings")

        for column in shipment_columns:
            shipment_table.heading(column, text=column)
            shipment_table.column(column, width=140)

        for row in get_shipments():
            shipment_table.insert("", tk.END, values=row)

        shipment_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        delivery_columns = ("delivery_id", "shipment_id", "delivery_date", "assigned_driver", "route_details")
        delivery_table = ttk.Treeview(deliveries_tab, columns=delivery_columns, show="headings")

        for column in delivery_columns:
            delivery_table.heading(column, text=column)
            delivery_table.column(column, width=160)

        for row in get_deliveries():
            delivery_table.insert("", tk.END, values=row)

        delivery_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        incident_columns = ("incident_id", "shipment_id", "incident_type", "incident_description")
        incident_table = ttk.Treeview(incidents_tab, columns=incident_columns, show="headings")

        for column in incident_columns:
            incident_table.heading(column, text=column)
            incident_table.column(column, width=180)

        for row in get_incidents():
            incident_table.insert("", tk.END, values=row)

        incident_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        inventory_columns = ("inventory_id", "item_name", "quantity", "reorder_level", "warehouse_location")
        inventory_table = ttk.Treeview(inventory_tab, columns=inventory_columns, show="headings")

        for column in inventory_columns:
            inventory_table.heading(column, text=column)
            inventory_table.column(column, width=180)

        for row in get_inventory():
            inventory_table.insert("", tk.END, values=row)

        inventory_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        vehicle_columns = ("vehicle_id", "capacity", "maintenance_schedule", "availability")
        vehicle_table = ttk.Treeview(vehicles_tab, columns=vehicle_columns, show="headings")

        for column in vehicle_columns:
            vehicle_table.heading(column, text=column)
            vehicle_table.column(column, width=180)

        for row in get_vehicles():
            vehicle_table.insert("", tk.END, values=row)

        vehicle_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def show_reports():
        clear_content()

        title = tk.Label(content_area, text="Generate Shipment Report", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
        title.pack(pady=20, padx=20, anchor="nw")

        form = tk.Frame(content_area, bg="#5293bb")
        form.pack(pady=10, padx=20, anchor="nw")

        tk.Label(form, text="Enter Shipment ID:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        shipment_id_entry = tk.Entry(form, width=50, font=("Courier New", 12))
        shipment_id_entry.pack(pady=5)

        result_box = tk.Text(content_area, font=("Courier New", 12), bg="#89cff1", fg="#003a6b")
        result_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        def generate():
            result_box.config(state=tk.NORMAL)
            result_box.delete(1.0, tk.END)

            if not shipment_id_entry.get().isdigit():
                title.config(text="Shipment ID must be numbers only")
                result_box.config(state=tk.DISABLED)
                return

            records = get_full_report(shipment_id_entry.get())

            if not records:
                result_box.insert(tk.END, "No data found for this shipment ID")
                result_box.config(state=tk.DISABLED)
                return

            for record in records:
                result_box.insert(tk.END, "SHIPMENT DETAILS\n")
                result_box.insert(tk.END, "-" * 50 + "\n")
                result_box.insert(tk.END, f"Shipment ID: {record[0]}\n")
                result_box.insert(tk.END, f"Order Number: {record[1]}\n")
                result_box.insert(tk.END, f"Sender: {record[2]}\n")
                result_box.insert(tk.END, f"Receiver: {record[3]}\n")
                result_box.insert(tk.END, f"Item: {record[4]}\n")
                result_box.insert(tk.END, f"Delivery Status: {record[5]}\n")
                result_box.insert(tk.END, f"Transport Cost: £{record[6]}\n")
                result_box.insert(tk.END, f"Surcharge: £{record[7]}\n")
                result_box.insert(tk.END, f"Payment Status: {record[8]}\n\n")

                result_box.insert(tk.END, "DELIVERY DETAILS\n")
                result_box.insert(tk.END, "-" * 50 + "\n")
                result_box.insert(tk.END, f"Delivery Date: {record[9]}\n")
                result_box.insert(tk.END, f"Assigned Driver: {record[10]}\n")
                result_box.insert(tk.END, f"Route Details: {record[11]}\n\n")

                result_box.insert(tk.END, "INCIDENT DETAILS\n")
                result_box.insert(tk.END, "-" * 50 + "\n")
                result_box.insert(tk.END, f"Incident Type: {record[12]}\n")
                result_box.insert(tk.END, f"Incident Description: {record[13]}\n")
                result_box.insert(tk.END, "=" * 70 + "\n\n")

            result_box.config(state=tk.DISABLED)

        tk.Button(form, text="Generate Report", command=generate, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=10)

    tk.Button(menu_area, text="Home", command=home, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2).pack(pady=10, padx=20)
    tk.Button(menu_area, text="Shipments", command=show_shipments, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2).pack(pady=10, padx=20)
    tk.Button(menu_area, text="Deliveries", command=show_deliveries, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2).pack(pady=10, padx=20)
    tk.Button(menu_area, text="Incidents", command=show_incidents, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2).pack(pady=10, padx=20)
    tk.Button(menu_area, text="Inventory", command=show_inventory, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2).pack(pady=10, padx=20)
    tk.Button(menu_area, text="Vehicles", command=show_vehicles, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2).pack(pady=10, padx=20)
    tk.Button(menu_area, text="Tables", command=show_tables, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2).pack(pady=10, padx=20)
    tk.Button(menu_area, text="Reports", command=show_reports, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2).pack(pady=10, padx=20)

    def close_app():
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", close_app)

    window.mainloop()