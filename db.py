import sqlite3
import hashlib
import logging


system_logger = logging.getLogger("system_logger")
system_logger.setLevel(logging.INFO)
system_handler = logging.FileHandler("system.log")
system_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
system_logger.addHandler(system_handler)

vehicle_logger = logging.getLogger("vehicle_logger")
vehicle_logger.setLevel(logging.INFO)
vehicle_handler = logging.FileHandler("vehicle.log")
vehicle_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
vehicle_logger.addHandler(vehicle_handler)

inventory_logger = logging.getLogger("inventory_logger")
inventory_logger.setLevel(logging.INFO)
inventory_handler = logging.FileHandler("inventory.log")
inventory_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
inventory_logger.addHandler(inventory_handler)


def log_action(action):
    system_logger.info(action)


def log_vehicle(action):
    vehicle_logger.info(action)


def log_inventory(action):
    inventory_logger.info(action)


def encrypt_data(data):
    if data is None:
        return ""

    encrypted = ""
    key = 7

    for letter in data:
        encrypted += chr(ord(letter) + key)

    return encrypted


def decrypt_data(data):
    if data is None:
        return ""

    decrypted = ""
    key = 7

    for letter in data:
        decrypted += chr(ord(letter) - key)

    return decrypted


def database():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS shipments (shipment_id INTEGER PRIMARY KEY, order_number TEXT, sender_details TEXT, receiver_details TEXT, item_description TEXT, delivery_status TEXT, transport_cost REAL, surcharge REAL, payment_status TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS shipment_updates (update_id INTEGER PRIMARY KEY, shipment_id INTEGER, update_date TEXT, update_status TEXT, update_notes TEXT, FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id))")

    cur.execute("CREATE TABLE IF NOT EXISTS deliveries (delivery_id INTEGER PRIMARY KEY, shipment_id INTEGER, delivery_date TEXT, assigned_driver TEXT, route_details TEXT, FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id))")

    cur.execute("CREATE TABLE IF NOT EXISTS incidents (incident_id INTEGER PRIMARY KEY, shipment_id INTEGER, incident_type TEXT, incident_description TEXT, FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id))")

    cur.execute("CREATE TABLE IF NOT EXISTS inventory (inventory_id INTEGER PRIMARY KEY, item_name TEXT, quantity INTEGER, reorder_level INTEGER, warehouse_location TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS vehicles (vehicle_id INTEGER PRIMARY KEY, capacity INTEGER, maintenance_schedule TEXT, availability TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS drivers (driver_id INTEGER PRIMARY KEY, driver_name TEXT, licence_number TEXT, route_history TEXT, shift_assignment TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS warehouse_logs (log_id INTEGER PRIMARY KEY, activity_type TEXT, item_name TEXT, quantity INTEGER, source_location TEXT, destination_location TEXT, activity_date TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS vehicle_logs (log_id INTEGER PRIMARY KEY, vehicle_id INTEGER, usage_type TEXT, usage_date TEXT, notes TEXT, FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id))")

    con.commit()
    con.close()

    log_action("Database initialised")


def users_exist():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    result = cur.fetchone()
    con.close()

    if result[0] > 0:
        return True

    return False


def add_user(username, password, role):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()

    hashed = hashlib.sha256(password.encode()).hexdigest()

    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, role))

    con.commit()
    con.close()

    log_action(f"User created: {username}")


def check_login(username, password):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()

    hashed = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, hashed))

    result = cur.fetchone()
    con.close()

    if result:
        log_action(f"Login success: {username}")
        return result[0]

    log_action(f"Login failed: {username}")
    return None


def add_shipment(order_number, sender_details, receiver_details, item_description, delivery_status, transport_cost, surcharge, payment_status):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()

    sender_details = encrypt_data(sender_details)
    receiver_details = encrypt_data(receiver_details)

    cur.execute("INSERT INTO shipments (order_number, sender_details, receiver_details, item_description, delivery_status, transport_cost, surcharge, payment_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (order_number, sender_details, receiver_details, item_description, delivery_status, transport_cost, surcharge, payment_status))

    shipment_id = cur.lastrowid

    cur.execute("INSERT INTO shipment_updates (shipment_id, update_date, update_status, update_notes) VALUES (?, ?, ?, ?)", (shipment_id, "Initial entry", delivery_status, "Shipment record created"))

    con.commit()
    con.close()

    log_action(f"Shipment added: {order_number}")


def add_shipment_update(shipment_id, update_date, update_status, update_notes):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()

    cur.execute("INSERT INTO shipment_updates (shipment_id, update_date, update_status, update_notes) VALUES (?, ?, ?, ?)", (shipment_id, update_date, update_status, update_notes))

    cur.execute("UPDATE shipments SET delivery_status = ? WHERE shipment_id = ?", (update_status, shipment_id))

    con.commit()
    con.close()

    log_action(f"Shipment update added: {shipment_id} - {update_status}")


def add_delivery(shipment_id, delivery_date, assigned_driver, route_details):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO deliveries (shipment_id, delivery_date, assigned_driver, route_details) VALUES (?, ?, ?, ?)", (shipment_id, delivery_date, assigned_driver, route_details))
    con.commit()
    con.close()

    log_action(f"Delivery added: {shipment_id}")


def add_incident(shipment_id, incident_type, incident_description):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO incidents (shipment_id, incident_type, incident_description) VALUES (?, ?, ?)", (shipment_id, incident_type, incident_description))
    con.commit()
    con.close()

    log_action(f"Incident added: {shipment_id}")


def add_inventory(item_name, quantity, reorder_level, warehouse_location):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO inventory (item_name, quantity, reorder_level, warehouse_location) VALUES (?, ?, ?, ?)", (item_name, quantity, reorder_level, warehouse_location))
    con.commit()
    con.close()

    log_inventory(f"Inventory added: {item_name}, quantity: {quantity}, reorder level: {reorder_level}, location: {warehouse_location}")


def add_vehicle(vehicle_id, capacity, maintenance_schedule, availability):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO vehicles (vehicle_id, capacity, maintenance_schedule, availability) VALUES (?, ?, ?, ?)", (vehicle_id, capacity, maintenance_schedule, availability))
    con.commit()
    con.close()

    log_vehicle(f"Vehicle added: {vehicle_id}, capacity: {capacity}, maintenance: {maintenance_schedule}, availability: {availability}")


def add_driver(driver_name, licence_number, route_history, shift_assignment):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()

    licence_number = encrypt_data(licence_number)

    cur.execute("INSERT INTO drivers (driver_name, licence_number, route_history, shift_assignment) VALUES (?, ?, ?, ?)", (driver_name, licence_number, route_history, shift_assignment))

    con.commit()
    con.close()

    log_action(f"Driver added: {driver_name}")


def add_warehouse_log(activity_type, item_name, quantity, source_location, destination_location, activity_date):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO warehouse_logs (activity_type, item_name, quantity, source_location, destination_location, activity_date) VALUES (?, ?, ?, ?, ?, ?)", (activity_type, item_name, quantity, source_location, destination_location, activity_date))
    con.commit()
    con.close()

    log_inventory(f"Warehouse activity: {activity_type}, item: {item_name}, quantity: {quantity}, source: {source_location}, destination: {destination_location}, date: {activity_date}")


def add_vehicle_log(vehicle_id, usage_type, usage_date, notes):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO vehicle_logs (vehicle_id, usage_type, usage_date, notes) VALUES (?, ?, ?, ?)", (vehicle_id, usage_type, usage_date, notes))
    con.commit()
    con.close()

    log_vehicle(f"Vehicle utilisation: {vehicle_id}, usage type: {usage_type}, date: {usage_date}, notes: {notes}")


def get_shipments():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM shipments")
    data = cur.fetchall()
    con.close()

    decrypted_data = []

    for row in data:
        decrypted_row = (
            row[0],
            row[1],
            decrypt_data(row[2]),
            decrypt_data(row[3]),
            row[4],
            row[5],
            row[6],
            row[7],
            row[8]
        )

        decrypted_data.append(decrypted_row)

    return decrypted_data


def get_shipment_updates():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM shipment_updates")
    data = cur.fetchall()
    con.close()
    return data


def get_updates_for_shipment(shipment_id):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT update_date, update_status, update_notes FROM shipment_updates WHERE shipment_id = ? ORDER BY update_id", (shipment_id,))
    data = cur.fetchall()
    con.close()
    return data


def get_deliveries():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM deliveries")
    data = cur.fetchall()
    con.close()
    return data


def get_incidents():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM incidents")
    data = cur.fetchall()
    con.close()
    return data


def get_inventory():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM inventory")
    data = cur.fetchall()
    con.close()
    return data


def get_vehicles():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vehicles")
    data = cur.fetchall()
    con.close()
    return data


def get_drivers():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM drivers")
    data = cur.fetchall()
    con.close()

    decrypted_data = []

    for row in data:
        decrypted_row = (
            row[0],
            row[1],
            decrypt_data(row[2]),
            row[3],
            row[4]
        )

        decrypted_data.append(decrypted_row)

    return decrypted_data


def get_warehouse_logs():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM warehouse_logs")
    data = cur.fetchall()
    con.close()
    return data


def get_vehicle_logs():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM vehicle_logs")
    data = cur.fetchall()
    con.close()
    return data


def get_users():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("SELECT user_id, username, role FROM users")
    data = cur.fetchall()
    con.close()
    return data


def get_full_report(shipment_id):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()

    cur.execute("""
    SELECT
        shipments.shipment_id,
        shipments.order_number,
        shipments.sender_details,
        shipments.receiver_details,
        shipments.item_description,
        shipments.delivery_status,
        shipments.transport_cost,
        shipments.surcharge,
        shipments.payment_status,
        deliveries.delivery_date,
        deliveries.assigned_driver,
        deliveries.route_details,
        incidents.incident_type,
        incidents.incident_description
    FROM shipments
    LEFT JOIN deliveries ON shipments.shipment_id = deliveries.shipment_id
    LEFT JOIN incidents ON shipments.shipment_id = incidents.shipment_id
    WHERE shipments.shipment_id = ?
    """, (shipment_id,))

    data = cur.fetchall()
    con.close()

    decrypted_data = []

    for row in data:
        decrypted_row = list(row)

        if decrypted_row[2] is not None:
            decrypted_row[2] = decrypt_data(decrypted_row[2])

        if decrypted_row[3] is not None:
            decrypted_row[3] = decrypt_data(decrypted_row[3])

        decrypted_data.append(tuple(decrypted_row))

    log_action(f"Report generated: {shipment_id}")

    return decrypted_data