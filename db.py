import sqlite3

def database():
    con = sqlite3.connect('northshore.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS shipments (shipment_id INTEGER PRIMARY KEY, order_number TEXT, sender_details TEXT, receiver_details TEXT, item_description TEXT)")
    con.commit()
    con.close()
