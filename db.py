import sqlite3

def database():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS shipments (shipment_id INTEGER PRIMARY KEY, order_number TEXT, sender_details TEXT, receiver_details TEXT, item_description TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS deliveries (delivery_id INTEGER PRIMARY KEY, shipment_id INTEGER, delivery_date TEXT, assigned_driver TEXT, route_details TEXT, FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id))")
    con.commit()
    con.close()

def add_shipment(order_number, sender_details, receiver_details, item_description):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO shipments (order_number, sender_details, receiver_details, item_description) VALUES (?, ?, ?, ?)", (order_number, sender_details, receiver_details, item_description))
    con.commit()
    con.close()

def add_delivery(shipment_id, delivery_date, assigned_driver, route_details):
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("INSERT INTO deliveries (shipment_id, delivery_date, assigned_driver, route_details) VALUES (?, ?, ?, ?)", (shipment_id, delivery_date, assigned_driver, route_details))
    con.commit()
    con.close()