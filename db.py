import sqlite3
import hashlib
import logging

logging.basicConfig(filename='system.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def log_action(action):
    logging.info(action)


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

    cur.execute("CREATE TABLE IF NOT EXISTS deliveries (delivery_id INTEGER PRIMARY KEY, shipment_id INTEGER, delivery_date TEXT, assigned_driver TEXT, route_details TEXT, FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id))")

    cur.execute("CREATE TABLE IF NOT EXISTS incidents (incident_id INTEGER PRIMARY KEY, shipment_id INTEGER, incident_type TEXT, incident_description TEXT, FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id))")

    cur.execute("CREATE TABLE IF NOT EXISTS inventory (inventory_id INTEGER PRIMARY KEY, item_name TEXT, quantity INTEGER, reorder_level INTEGER, warehouse_location TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS vehicles (vehicle_id INTEGER PRIMARY KEY, capacity INTEGER, maintenance_schedule TEXT, availability TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS drivers (driver_id INTEGER PRIMARY KEY, driver_name TEXT, licence_number TEXT, route_history TEXT, shift_assignment TEXT)")

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

    con.commit()
    con.close()

    log_action(f"Shipment added: {order_number}")


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

    log_action(f"Inventory added: {item_name}")


def add_vehicle(capacity, maintenance_schedule, availability):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO vehicles (capacity, maintenance_schedule, availability) VALUES (?, ?, ?)", (capacity, maintenance_schedule, availability))
    con.commit()
    con.close()

    log_action("Vehicle added")


def add_driver(driver_name, licence_number, route_history, shift_assignment):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()

    licence_number = encrypt_data(licence_number)

    cur.execute("INSERT INTO drivers (driver_name, licence_number, route_history, shift_assignment) VALUES (?, ?, ?, ?)", (driver_name, licence_number, route_history, shift_assignment))

    con.commit()
    con.close()

    log_action(f"Driver added: {driver_name}")


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


def get_full_report(shipment_id):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()

    cur.execute("""
    SELECT *
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