import sqlite3
import hashlib


def database():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS shipments (shipment_id INTEGER PRIMARY KEY, order_number TEXT, sender_details TEXT, receiver_details TEXT, item_description TEXT, delivery_status TEXT, transport_cost REAL, surcharge REAL, payment_status TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS deliveries (delivery_id INTEGER PRIMARY KEY, shipment_id INTEGER, delivery_date TEXT, assigned_driver TEXT, route_details TEXT, FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id))")

    cur.execute("CREATE TABLE IF NOT EXISTS incidents (incident_id INTEGER PRIMARY KEY, shipment_id INTEGER, incident_type TEXT, incident_description TEXT, FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id))")

    cur.execute("CREATE TABLE IF NOT EXISTS inventory (inventory_id INTEGER PRIMARY KEY, item_name TEXT, quantity INTEGER, reorder_level INTEGER, warehouse_location TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS vehicles (vehicle_id INTEGER PRIMARY KEY, capacity INTEGER, maintenance_schedule TEXT, availability TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS drivers (driver_id INTEGER PRIMARY KEY, driver_name TEXT, licence_number TEXT, route_history TEXT, shift_assignment TEXT)")

    cur.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    existing_user = cur.fetchone()

    if existing_user is None:
        password = hashlib.sha256("admin123".encode()).hexdigest()
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", password, "admin"))

    con.commit()
    con.close()


def check_login(username, password):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, hashed_password))

    result = cur.fetchone()

    con.close()

    if result:
        return result[0]

    return None


def add_shipment(order_number, sender_details, receiver_details, item_description, delivery_status, transport_cost, surcharge, payment_status):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO shipments (order_number, sender_details, receiver_details, item_description, delivery_status, transport_cost, surcharge, payment_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (order_number, sender_details, receiver_details, item_description, delivery_status, transport_cost, surcharge, payment_status))
    con.commit()
    con.close()


def add_delivery(shipment_id, delivery_date, assigned_driver, route_details):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO deliveries (shipment_id, delivery_date, assigned_driver, route_details) VALUES (?, ?, ?, ?)", (shipment_id, delivery_date, assigned_driver, route_details))
    con.commit()
    con.close()


def add_incident(shipment_id, incident_type, incident_description):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO incidents (shipment_id, incident_type, incident_description) VALUES (?, ?, ?)", (shipment_id, incident_type, incident_description))
    con.commit()
    con.close()


def add_inventory(item_name, quantity, reorder_level, warehouse_location):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO inventory (item_name, quantity, reorder_level, warehouse_location) VALUES (?, ?, ?, ?)", (item_name, quantity, reorder_level, warehouse_location))
    con.commit()
    con.close()


def add_vehicle(capacity, maintenance_schedule, availability):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO vehicles (capacity, maintenance_schedule, availability) VALUES (?, ?, ?)", (capacity, maintenance_schedule, availability))
    con.commit()
    con.close()


def add_driver(driver_name, licence_number, route_history, shift_assignment):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO drivers (driver_name, licence_number, route_history, shift_assignment) VALUES (?, ?, ?, ?)", (driver_name, licence_number, route_history, shift_assignment))
    con.commit()
    con.close()


def get_shipments():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM shipments")
    records = cur.fetchall()
    con.close()
    return records


def get_deliveries():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM deliveries")
    records = cur.fetchall()
    con.close()
    return records


def get_incidents():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM incidents")
    records = cur.fetchall()
    con.close()
    return records


def get_inventory():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM inventory")
    records = cur.fetchall()
    con.close()
    return records


def get_vehicles():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vehicles")
    records = cur.fetchall()
    con.close()
    return records


def get_drivers():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM drivers")
    records = cur.fetchall()
    con.close()
    return records


def get_full_report(shipment_id):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()

    cur.execute("SELECT shipments.shipment_id, shipments.order_number, shipments.sender_details, shipments.receiver_details, shipments.item_description, shipments.delivery_status, shipments.transport_cost, shipments.surcharge, shipments.payment_status, deliveries.delivery_date, deliveries.assigned_driver, deliveries.route_details, incidents.incident_type, incidents.incident_description FROM shipments LEFT JOIN deliveries ON shipments.shipment_id = deliveries.shipment_id LEFT JOIN incidents ON shipments.shipment_id = incidents.shipment_id WHERE shipments.shipment_id = ?", (shipment_id,))

    records = cur.fetchall()
    con.close()
    return records