import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
from db import *


def app():
    window = tk.Tk()
    window.title("Database Application")
    window.geometry("1700x900")

    logged_in_role = {"role": None}

    def clear_window():
        for widget in window.winfo_children():
            widget.destroy()

    def show_create_admin():
        clear_window()

        login_frame = tk.Frame(window, bg="#003a6b")
        login_frame.pack(fill=tk.BOTH, expand=True)

        login_box = tk.Frame(login_frame, bg="#5293bb", padx=40, pady=40)
        login_box.pack(expand=True)

        title = tk.Label(login_box, text="Create Admin Account", bg="#89cff1", fg="#003a6b", font=("Courier New", 18, "bold"), padx=20, pady=10)
        title.pack(pady=20)

        tk.Label(login_box, text="Username:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        username_entry = tk.Entry(login_box, width=40, font=("Courier New", 12))
        username_entry.pack(pady=5)

        tk.Label(login_box, text="Password:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        password_entry = tk.Entry(login_box, width=40, font=("Courier New", 12), show="*")
        password_entry.pack(pady=5)

        def create_admin():
            if username_entry.get() == "" or password_entry.get() == "":
                title.config(text="Fill all fields")
                return

            add_user(username_entry.get(), password_entry.get(), "admin")
            show_login()

        tk.Button(login_box, text="Create Admin", command=create_admin, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=20)

    def show_login():
        clear_window()

        login_frame = tk.Frame(window, bg="#003a6b")
        login_frame.pack(fill=tk.BOTH, expand=True)

        login_box = tk.Frame(login_frame, bg="#5293bb", padx=40, pady=40)
        login_box.pack(expand=True)

        title = tk.Label(login_box, text="Northshore Logistics Login", bg="#89cff1", fg="#003a6b", font=("Courier New", 18, "bold"), padx=20, pady=10)
        title.pack(pady=20)

        tk.Label(login_box, text="Username:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        username_entry = tk.Entry(login_box, width=40, font=("Courier New", 12))
        username_entry.pack(pady=5)

        tk.Label(login_box, text="Password:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
        password_entry = tk.Entry(login_box, width=40, font=("Courier New", 12), show="*")
        password_entry.pack(pady=5)

        def login():
            role = check_login(username_entry.get(), password_entry.get())

            if role:
                logged_in_role["role"] = role
                show_main_app()
            else:
                title.config(text="Invalid login details")

        tk.Button(login_box, text="Login", command=login, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=20)

    def show_main_app():
        clear_window()

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

            role_label = tk.Label(content_area, text=f"Logged in as: {logged_in_role['role']}", bg="#89cff1", fg="#003a6b", font=("Courier New", 12), padx=20, pady=10)
            role_label.pack(pady=10, padx=20, anchor="nw")

        def show_users():
            clear_content()

            title = tk.Label(content_area, text="User Management", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
            title.pack(pady=20, padx=20, anchor="nw")

            form = tk.Frame(content_area, bg="#5293bb")
            form.pack(pady=10, padx=20, anchor="nw")

            tk.Label(form, text="Username:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            username_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            username_entry.pack(pady=5)

            tk.Label(form, text="Password:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            password_entry = tk.Entry(form, width=50, font=("Courier New", 12), show="*")
            password_entry.pack(pady=5)

            tk.Label(form, text="Role:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            role_entry = ttk.Combobox(form, values=["Select Role", "admin", "manager", "warehouse", "driver"], font=("Courier New", 12), width=47, state="readonly")
            role_entry.pack(pady=5)
            role_entry.current(0)

            def submit_user():
                if username_entry.get() == "":
                    title.config(text="Username is required")
                    return

                if password_entry.get() == "":
                    title.config(text="Password is required")
                    return

                if role_entry.get() == "Select Role":
                    title.config(text="Select role")
                    return

                try:
                    add_user(username_entry.get(), password_entry.get(), role_entry.get())
                    title.config(text="User added")

                    username_entry.delete(0, tk.END)
                    password_entry.delete(0, tk.END)
                    role_entry.current(0)

                    window.after(1000, lambda: title.config(text="User Management"))
                except sqlite3.IntegrityError:
                    title.config(text="Username already exists")

            tk.Button(form, text="Add User", command=submit_user, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=15)

            user_columns = ("user_id", "username", "role")
            user_table = ttk.Treeview(content_area, columns=user_columns, show="headings")

            for column in user_columns:
                user_table.heading(column, text=column)
                user_table.column(column, width=180)

            for row in get_users():
                user_table.insert("", tk.END, values=row)

            user_table.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

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

        def show_shipment_updates():
            clear_content()

            title = tk.Label(content_area, text="Shipment Update History", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
            title.pack(pady=20, padx=20, anchor="nw")

            form = tk.Frame(content_area, bg="#5293bb")
            form.pack(pady=10, padx=20, anchor="nw")

            tk.Label(form, text="Order Number:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            order_number_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            order_number_entry.pack(pady=5)

            tk.Label(form, text="Update Date:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            update_date_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            update_date_entry.pack(pady=5)

            tk.Label(form, text="Update Status:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            update_status_entry = ttk.Combobox(form, values=["Select Update Status", "Dispatched", "In Transit", "Out for Delivery", "Delayed", "Returned to Warehouse", "Delivered"], font=("Courier New", 12), width=47, state="readonly")
            update_status_entry.pack(pady=5)
            update_status_entry.current(0)

            tk.Label(form, text="Update Notes:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            update_notes_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            update_notes_entry.pack(pady=5)

            def submit_update():
                if order_number_entry.get() == "":
                    title.config(text="Order number is required")
                    return

                if update_status_entry.get() == "Select Update Status":
                    title.config(text="Select update status")
                    return

                success = add_shipment_update(order_number_entry.get(), update_date_entry.get(), update_status_entry.get(), update_notes_entry.get())

                if not success:
                    title.config(text="Order number not found")
                    return

                title.config(text="Shipment update added")

                order_number_entry.delete(0, tk.END)
                update_date_entry.delete(0, tk.END)
                update_status_entry.current(0)
                update_notes_entry.delete(0, tk.END)

                window.after(1000, lambda: title.config(text="Shipment Update History"))

            tk.Button(form, text="Add Update", command=submit_update, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=15)

        def show_deliveries():
            clear_content()

            title = tk.Label(content_area, text="Add Delivery", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
            title.pack(pady=20, padx=20, anchor="nw")

            form = tk.Frame(content_area, bg="#5293bb")
            form.pack(pady=10, padx=20, anchor="nw")

            tk.Label(form, text="Order Number:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            order_number_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            order_number_entry.pack(pady=5)

            tk.Label(form, text="Delivery Date:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            delivery_date_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            delivery_date_entry.pack(pady=5)

            tk.Label(form, text="Assigned Driver:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            assigned_driver_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            assigned_driver_entry.pack(pady=5)

            tk.Label(form, text="Route Details (start - end):", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            route_details_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            route_details_entry.pack(pady=5)

            def submit_delivery():
                if order_number_entry.get() == "":
                    title.config(text="Order number is required")
                    return

                success = add_delivery(order_number_entry.get(), delivery_date_entry.get(), assigned_driver_entry.get(), route_details_entry.get())

                if not success:
                    title.config(text="Order number not found")
                    return

                title.config(text="Delivery added")

                order_number_entry.delete(0, tk.END)
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

            tk.Label(form, text="Order Number:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            order_number_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            order_number_entry.pack(pady=5)

            tk.Label(form, text="Incident Type:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            incident_type_entry = ttk.Combobox(form, values=["Select Incident Type", "Crash", "Transport Delay", "Delivery Delay", "Damaged Goods", "Failed Delivery Attempt", "Route Change", "Other"], font=("Courier New", 12), width=47, state="readonly")
            incident_type_entry.pack(pady=5)
            incident_type_entry.current(0)

            tk.Label(form, text="Incident Description:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            incident_description_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            incident_description_entry.pack(pady=5)

            def submit_incident():
                if order_number_entry.get() == "":
                    title.config(text="Order number is required")
                    return

                if incident_type_entry.get() == "Select Incident Type":
                    title.config(text="Select incident type")
                    return

                success = add_incident(order_number_entry.get(), incident_type_entry.get(), incident_description_entry.get())

                if not success:
                    title.config(text="Order number not found")
                    return

                title.config(text="Incident added")

                order_number_entry.delete(0, tk.END)
                incident_type_entry.current(0)
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

            tk.Label(form, text="Vehicle ID:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            vehicle_id_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            vehicle_id_entry.pack(pady=5)

            tk.Label(form, text="Vehicle Capacity (kg):", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
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
                if not vehicle_id_entry.get().isdigit():
                    title.config(text="Vehicle ID must be numbers only")
                    return

                if not capacity_entry.get().isdigit():
                    title.config(text="Vehicle capacity must be numbers only")
                    return

                if availability_entry.get() == "Select Availability":
                    title.config(text="Select availability")
                    return

                try:
                    add_vehicle(vehicle_id_entry.get(), capacity_entry.get(), maintenance_schedule_entry.get(), availability_entry.get())
                    title.config(text="Vehicle added")
                except sqlite3.IntegrityError:
                    title.config(text="Vehicle ID already exists")
                    return

                vehicle_id_entry.delete(0, tk.END)
                capacity_entry.delete(0, tk.END)
                maintenance_schedule_entry.delete(0, tk.END)
                availability_entry.current(0)

                window.after(1000, lambda: title.config(text="Vehicle Management"))

            tk.Button(form, text="Add Vehicle", command=submit_vehicle, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=15)

        def show_drivers():
            clear_content()

            title = tk.Label(content_area, text="Driver Management", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
            title.pack(pady=20, padx=20, anchor="nw")

            form = tk.Frame(content_area, bg="#5293bb")
            form.pack(pady=10, padx=20, anchor="nw")

            tk.Label(form, text="Driver Name:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            driver_name_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            driver_name_entry.pack(pady=5)

            tk.Label(form, text="Licence Number:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            licence_number_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            licence_number_entry.pack(pady=5)

            tk.Label(form, text="Shift Assignment:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            shift_assignment_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            shift_assignment_entry.pack(pady=5)

            def submit_driver():
                route_history = "Recorded through delivery route assignments"
                add_driver(driver_name_entry.get(), licence_number_entry.get(), route_history, shift_assignment_entry.get())

                title.config(text="Driver added")

                driver_name_entry.delete(0, tk.END)
                licence_number_entry.delete(0, tk.END)
                shift_assignment_entry.delete(0, tk.END)

                window.after(1000, lambda: title.config(text="Driver Management"))

            tk.Button(form, text="Add Driver", command=submit_driver, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=15)

        def show_warehouse_activity():
            clear_content()

            title = tk.Label(content_area, text="Warehouse Activity", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
            title.pack(pady=20, padx=20, anchor="nw")

            form = tk.Frame(content_area, bg="#5293bb")
            form.pack(pady=10, padx=20, anchor="nw")

            tk.Label(form, text="Activity Type:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            activity_type_entry = ttk.Combobox(form, values=["Select Activity Type", "Inbound", "Outbound", "Restocking", "Item Transfer"], font=("Courier New", 12), width=47, state="readonly")
            activity_type_entry.pack(pady=5)
            activity_type_entry.current(0)

            tk.Label(form, text="Item Name:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            item_name_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            item_name_entry.pack(pady=5)

            tk.Label(form, text="Quantity:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            quantity_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            quantity_entry.pack(pady=5)

            tk.Label(form, text="Source Location:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            source_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            source_entry.pack(pady=5)

            tk.Label(form, text="Destination Location:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            destination_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            destination_entry.pack(pady=5)

            tk.Label(form, text="Activity Date:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            activity_date_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            activity_date_entry.pack(pady=5)

            def submit_warehouse_activity():
                if activity_type_entry.get() == "Select Activity Type":
                    title.config(text="Select activity type")
                    return

                if not quantity_entry.get().isdigit():
                    title.config(text="Quantity must be numbers only")
                    return

                add_warehouse_log(activity_type_entry.get(), item_name_entry.get(), quantity_entry.get(), source_entry.get(), destination_entry.get(), activity_date_entry.get())

                title.config(text="Warehouse activity added")

                activity_type_entry.current(0)
                item_name_entry.delete(0, tk.END)
                quantity_entry.delete(0, tk.END)
                source_entry.delete(0, tk.END)
                destination_entry.delete(0, tk.END)
                activity_date_entry.delete(0, tk.END)

                window.after(1000, lambda: title.config(text="Warehouse Activity"))

            tk.Button(form, text="Add Activity", command=submit_warehouse_activity, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=15)

        def show_vehicle_utilisation():
            clear_content()

            title = tk.Label(content_area, text="Vehicle Utilisation", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
            title.pack(pady=20, padx=20, anchor="nw")

            form = tk.Frame(content_area, bg="#5293bb")
            form.pack(pady=10, padx=20, anchor="nw")

            tk.Label(form, text="Vehicle ID:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            vehicle_id_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            vehicle_id_entry.pack(pady=5)

            tk.Label(form, text="Usage Type:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            usage_type_entry = ttk.Combobox(form, values=["Select Usage Type", "Delivery", "Collection", "Transfer", "Maintenance"], font=("Courier New", 12), width=47, state="readonly")
            usage_type_entry.pack(pady=5)
            usage_type_entry.current(0)

            tk.Label(form, text="Usage Date:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            usage_date_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            usage_date_entry.pack(pady=5)

            tk.Label(form, text="Notes:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            notes_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            notes_entry.pack(pady=5)

            def submit_vehicle_utilisation():
                if not vehicle_id_entry.get().isdigit():
                    title.config(text="Vehicle ID must be numbers only")
                    return

                if usage_type_entry.get() == "Select Usage Type":
                    title.config(text="Select usage type")
                    return

                add_vehicle_log(vehicle_id_entry.get(), usage_type_entry.get(), usage_date_entry.get(), notes_entry.get())

                title.config(text="Vehicle utilisation added")

                vehicle_id_entry.delete(0, tk.END)
                usage_type_entry.current(0)
                usage_date_entry.delete(0, tk.END)
                notes_entry.delete(0, tk.END)

                window.after(1000, lambda: title.config(text="Vehicle Utilisation"))

            tk.Button(form, text="Add Utilisation", command=submit_vehicle_utilisation, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=15)

        def show_manage_records():
            clear_content()

            title = tk.Label(content_area, text="Manage Records", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
            title.pack(pady=20, padx=20, anchor="nw")

            form = tk.Frame(content_area, bg="#5293bb")
            form.pack(pady=10, padx=20, anchor="nw")

            tk.Label(form, text="Table:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            table_entry = ttk.Combobox(form, values=["Select Table", "Users", "Shipments", "Shipment Updates", "Deliveries", "Incidents", "Inventory", "Vehicles", "Drivers", "Warehouse Activity", "Vehicle Utilisation"], font=("Courier New", 12), width=47, state="readonly")
            table_entry.pack(pady=5)
            table_entry.current(0)

            tk.Label(form, text="Record Identifier:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            record_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            record_entry.pack(pady=5)

            identifier_note = tk.Label(form, text="Use order number for Shipments. Use row ID for other tables.", bg="#5293bb", fg="#003a6b", font=("Courier New", 10, "bold"))
            identifier_note.pack(anchor="w", pady=5)

            tk.Label(form, text="Field to Edit:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            field_entry = ttk.Combobox(form, values=["Select Field"], font=("Courier New", 12), width=47, state="readonly")
            field_entry.pack(pady=5)
            field_entry.current(0)

            tk.Label(form, text="New Value:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            value_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            value_entry.pack(pady=5)

            tk.Label(form, text="Order Number for Full History Delete:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            history_order_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            history_order_entry.pack(pady=5)

            def update_fields(event):
                selected_table = table_entry.get()

                if selected_table == "Select Table":
                    field_entry.config(values=["Select Field"])
                    field_entry.current(0)
                    return

                fields = get_editable_fields(selected_table)
                field_entry.config(values=["Select Field"] + fields)
                field_entry.current(0)

            table_entry.bind("<<ComboboxSelected>>", update_fields)

            def submit_edit():
                if table_entry.get() == "Select Table":
                    title.config(text="Select table")
                    return

                if record_entry.get() == "":
                    title.config(text="Enter record identifier")
                    return

                if field_entry.get() == "Select Field":
                    title.config(text="Select field to edit")
                    return

                if value_entry.get() == "":
                    title.config(text="Enter new value")
                    return

                success = edit_record(table_entry.get(), record_entry.get(), field_entry.get(), value_entry.get())

                if not success:
                    title.config(text="Edit failed")
                    return

                title.config(text="Record edited")

                value_entry.delete(0, tk.END)

                window.after(1000, lambda: title.config(text="Manage Records"))

            def submit_delete_record():
                if table_entry.get() == "Select Table":
                    title.config(text="Select table")
                    return

                if record_entry.get() == "":
                    title.config(text="Enter record identifier")
                    return

                success = delete_record(table_entry.get(), record_entry.get())

                if not success:
                    title.config(text="Delete failed")
                    return

                title.config(text="Record deleted")

                record_entry.delete(0, tk.END)
                value_entry.delete(0, tk.END)

                window.after(1000, lambda: title.config(text="Manage Records"))

            def submit_delete_history():
                if history_order_entry.get() == "":
                    title.config(text="Enter order number for full history delete")
                    return

                success = delete_order_history(history_order_entry.get())

                if not success:
                    title.config(text="Order number not found")
                    return

                title.config(text="Order history deleted")

                history_order_entry.delete(0, tk.END)

                window.after(1000, lambda: title.config(text="Manage Records"))

            button_row = tk.Frame(form, bg="#5293bb")
            button_row.pack(pady=15, anchor="w")

            tk.Button(button_row, text="Edit Record", command=submit_edit, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=18).pack(side=tk.LEFT, padx=5)
            tk.Button(button_row, text="Delete Record", command=submit_delete_record, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=18).pack(side=tk.LEFT, padx=5)
            tk.Button(button_row, text="Delete History", command=submit_delete_history, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=18).pack(side=tk.LEFT, padx=5)

            help_box = tk.Text(content_area, font=("Courier New", 12), bg="#89cff1", fg="#003a6b", height=10)
            help_box.pack(fill=tk.X, padx=20, pady=10)

            help_box.insert(tk.END, "Manage Records Guide\n")
            help_box.insert(tk.END, "-" * 60 + "\n")
            help_box.insert(tk.END, "Edit Record: changes one existing value without creating history.\n")
            help_box.insert(tk.END, "Delete Record: removes one selected row. If Shipments is selected, it removes the shipment and linked order records.\n")
            help_box.insert(tk.END, "Delete History: removes shipment updates, deliveries and incidents for one order number, but keeps the main shipment record.\n")
            help_box.insert(tk.END, "For Shipments, use the order number as the record identifier.\n")
            help_box.insert(tk.END, "For other tables, use the row ID shown in the Tables screen.\n")
            help_box.config(state=tk.DISABLED)

        def show_tables():
            clear_content()

            title = tk.Label(content_area, text="Database Tables", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
            title.pack(pady=20, padx=20, anchor="nw")

            notebook = ttk.Notebook(content_area)
            notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            table_details = [
                ("Shipments", ("shipment_id", "order_number", "sender_details", "receiver_details", "item_description", "delivery_status", "transport_cost", "surcharge", "payment_status"), get_shipments),
                ("Shipment Updates", ("update_id", "order_number", "update_date", "update_status", "update_notes"), get_shipment_updates),
                ("Deliveries", ("delivery_id", "order_number", "delivery_date", "assigned_driver", "route_details"), get_deliveries),
                ("Incidents", ("incident_id", "order_number", "incident_type", "incident_description"), get_incidents),
                ("Inventory", ("inventory_id", "item_name", "quantity", "reorder_level", "warehouse_location"), get_inventory),
                ("Vehicles", ("vehicle_id", "capacity", "maintenance_schedule", "availability"), get_vehicles),
                ("Drivers", ("driver_id", "driver_name", "licence_number", "route_history", "shift_assignment"), get_drivers),
                ("Warehouse Activity", ("log_id", "activity_type", "item_name", "quantity", "source_location", "destination_location", "activity_date"), get_warehouse_logs),
                ("Vehicle Utilisation", ("log_id", "vehicle_id", "usage_type", "usage_date", "notes"), get_vehicle_logs)
            ]

            for table_name, columns, data_function in table_details:
                tab = tk.Frame(notebook, bg="#5293bb")
                notebook.add(tab, text=table_name)

                table = ttk.Treeview(tab, columns=columns, show="headings")

                for column in columns:
                    table.heading(column, text=column)
                    table.column(column, width=160)

                for row in data_function():
                    table.insert("", tk.END, values=row)

                table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        def show_reports():
            clear_content()

            title = tk.Label(content_area, text="Generate Shipment Report", bg="#89cff1", fg="#003a6b", font=("Courier New", 16, "bold"), padx=20, pady=10)
            title.pack(pady=20, padx=20, anchor="nw")

            form = tk.Frame(content_area, bg="#5293bb")
            form.pack(pady=10, padx=20, anchor="nw")

            tk.Label(form, text="Enter Order Number:", bg="#5293bb", fg="#003a6b", font=("Courier New", 12, "bold")).pack(anchor="w")
            order_number_entry = tk.Entry(form, width=50, font=("Courier New", 12))
            order_number_entry.pack(pady=5)

            result_box = tk.Text(content_area, font=("Courier New", 12), bg="#89cff1", fg="#003a6b")
            result_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            def generate():
                result_box.config(state=tk.NORMAL)
                result_box.delete(1.0, tk.END)

                if order_number_entry.get() == "":
                    title.config(text="Order number is required")
                    result_box.config(state=tk.DISABLED)
                    return

                records = get_full_report(order_number_entry.get())
                updates = get_updates_for_order(order_number_entry.get())

                if not records:
                    result_box.insert(tk.END, "No data found for this order number")
                    result_box.config(state=tk.DISABLED)
                    return

                result_box.insert(tk.END, "NORTHSHORE LOGISTICS SHIPMENT REPORT\n")
                result_box.insert(tk.END, "=" * 60 + "\n\n")

                first_record = records[0]

                result_box.insert(tk.END, "Shipment Details\n")
                result_box.insert(tk.END, "-" * 60 + "\n")
                result_box.insert(tk.END, f"Order Number      : {first_record[1]}\n")
                result_box.insert(tk.END, f"Sender Details    : {first_record[2]}\n")
                result_box.insert(tk.END, f"Receiver Details  : {first_record[3]}\n")
                result_box.insert(tk.END, f"Item Description  : {first_record[4]}\n")
                result_box.insert(tk.END, f"Current Status    : {first_record[5]}\n")
                result_box.insert(tk.END, f"Transport Cost    : £{first_record[6]}\n")
                result_box.insert(tk.END, f"Surcharge         : £{first_record[7]}\n")
                result_box.insert(tk.END, f"Payment Status    : {first_record[8]}\n\n")

                result_box.insert(tk.END, "Shipment Timeline\n")
                result_box.insert(tk.END, "-" * 60 + "\n")

                if updates:
                    for update in updates:
                        result_box.insert(tk.END, f"Date              : {update[0]}\n")
                        result_box.insert(tk.END, f"Status            : {update[1]}\n")
                        result_box.insert(tk.END, f"Notes             : {update[2]}\n\n")
                else:
                    result_box.insert(tk.END, "No shipment updates recorded.\n\n")

                result_box.insert(tk.END, "Delivery Details\n")
                result_box.insert(tk.END, "-" * 60 + "\n")

                delivery_found = False

                for record in records:
                    if record[9] is not None:
                        delivery_found = True
                        result_box.insert(tk.END, f"Delivery Date     : {record[9]}\n")
                        result_box.insert(tk.END, f"Assigned Driver   : {record[10]}\n")
                        result_box.insert(tk.END, f"Route Details     : {record[11]}\n\n")

                if not delivery_found:
                    result_box.insert(tk.END, "No delivery details recorded.\n\n")

                result_box.insert(tk.END, "Incident Details\n")
                result_box.insert(tk.END, "-" * 60 + "\n")

                incident_found = False

                for record in records:
                    if record[12] is not None:
                        incident_found = True
                        result_box.insert(tk.END, f"Incident Type     : {record[12]}\n")
                        result_box.insert(tk.END, f"Description       : {record[13]}\n\n")

                if not incident_found:
                    result_box.insert(tk.END, "No incidents recorded.\n\n")

                result_box.insert(tk.END, "=" * 60 + "\n")
                result_box.insert(tk.END, "End of report")

                result_box.config(state=tk.DISABLED)

            tk.Button(form, text="Generate Report", command=generate, bg="#89cff1", fg="#003a6b", font=("Courier New", 12, "bold"), width=20).pack(pady=10)

        def logout():
            logged_in_role["role"] = None
            show_login()

        home()

        home_btn = tk.Button(menu_area, text="Home", command=home, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        home_btn.pack(pady=4, padx=20)

        users_btn = tk.Button(menu_area, text="Users", command=show_users, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        users_btn.pack(pady=4, padx=20)

        shipments_btn = tk.Button(menu_area, text="Shipments", command=show_shipments, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        shipments_btn.pack(pady=4, padx=20)

        shipment_updates_btn = tk.Button(menu_area, text="Shipment Updates", command=show_shipment_updates, bg="#89cff1", fg="#003a6b", font=("Courier New", 13, "bold"), width=20, height=2)
        shipment_updates_btn.pack(pady=4, padx=20)

        deliveries_btn = tk.Button(menu_area, text="Deliveries", command=show_deliveries, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        deliveries_btn.pack(pady=4, padx=20)

        incidents_btn = tk.Button(menu_area, text="Incidents", command=show_incidents, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        incidents_btn.pack(pady=4, padx=20)

        inventory_btn = tk.Button(menu_area, text="Inventory", command=show_inventory, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        inventory_btn.pack(pady=4, padx=20)

        vehicles_btn = tk.Button(menu_area, text="Vehicles", command=show_vehicles, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        vehicles_btn.pack(pady=4, padx=20)

        drivers_btn = tk.Button(menu_area, text="Drivers", command=show_drivers, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        drivers_btn.pack(pady=4, padx=20)

        warehouse_activity_btn = tk.Button(menu_area, text="Warehouse Activity", command=show_warehouse_activity, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        warehouse_activity_btn.pack(pady=4, padx=20)

        vehicle_utilisation_btn = tk.Button(menu_area, text="Vehicle Utilisation", command=show_vehicle_utilisation, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        vehicle_utilisation_btn.pack(pady=4, padx=20)

        manage_records_btn = tk.Button(menu_area, text="Manage Records", command=show_manage_records, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        manage_records_btn.pack(pady=4, padx=20)

        tables_btn = tk.Button(menu_area, text="Tables", command=show_tables, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        tables_btn.pack(pady=4, padx=20)

        reports_btn = tk.Button(menu_area, text="Reports", command=show_reports, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        reports_btn.pack(pady=4, padx=20)

        logout_btn = tk.Button(menu_area, text="Logout", command=logout, bg="#89cff1", fg="#003a6b", font=("Courier New", 14, "bold"), width=20, height=2)
        logout_btn.pack(pady=4, padx=20)

        role = logged_in_role["role"]

        if role == "driver":
            users_btn.config(state="disabled")
            shipments_btn.config(state="disabled")
            inventory_btn.config(state="disabled")
            vehicles_btn.config(state="disabled")
            drivers_btn.config(state="disabled")
            warehouse_activity_btn.config(state="disabled")
            manage_records_btn.config(state="disabled")

        elif role == "warehouse":
            users_btn.config(state="disabled")
            vehicles_btn.config(state="disabled")
            drivers_btn.config(state="disabled")
            vehicle_utilisation_btn.config(state="disabled")

        elif role == "manager":
            users_btn.config(state="disabled")

    window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())

    if users_exist():
        show_login()
    else:
        show_create_admin()

    window.mainloop()