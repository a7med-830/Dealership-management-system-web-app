# database.py
import sqlite3
from datetime import datetime
import sqlite3
import os 

def connect_to_db():
    conn = sqlite3.connect('dealership.db')
    return conn

# Initialize the database tables
def initialize_database():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Cars (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        brand TEXT,
                        model TEXT,
                        year TEXT,
                        form TEXT,
                        price REAL,
                        availability TEXT
                     )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Bikes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        brand TEXT,
                        model TEXT,
                        year TEXT,
                        price REAL,
                        availability TEXT
                     )''')
    
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Purchases (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_name TEXT,
                        customer_phone TEXT,
                        vehicle_id INTEGER,
                        vehicle_type TEXT,
                        purchase_date TEXT
                    )''')

    conn.commit()
    conn.close()

def add_car_to_db(car):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Cars (brand, model, year, form, price, availability) VALUES (?, ?, ?, ?, ?, ?)',
                   (car.brand, car.model, car.year, car.form, car.price, 'Yes' if car.isAvailable else 'No'))

    conn.commit()
    conn.close()

def fetch_all_cars():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Cars')
    cars = cursor.fetchall()

    conn.close()
    return cars

def delete_car_from_db(id_num):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM Cars WHERE id = ?', (id_num,))
        conn.commit()
        print(f"Car with ID {id_num} has been deleted.")
    except sqlite3.Error as e:
        print(f"An error occurred while deleting the car: {e}")
    finally:
        conn.close()

def add_bike_to_db(bike):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Bikes (brand, model, year, price, availability) VALUES (?, ?, ?, ?, ?)',
                   (bike.brand, bike.model, bike.year, bike.price, 'Yes' if bike.isAvailable else 'No'))

    conn.commit()
    conn.close()

def fetch_all_bikes():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Bikes')
    bikes = cursor.fetchall()

    conn.close()
    return bikes

def delete_bike_from_db(id_num):
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM Bikes WHERE id = ?', (id_num,))
        conn.commit()
        print(f"Bike with ID {id_num} has been deleted.")
    except sqlite3.Error as e:
        print(f"An error occurred while deleting the bike: {e}")
    finally:
        conn.close()

def update_vehicle_availability(vehicle_type, vehicle_id, is_available):
    conn = connect_to_db()
    cursor = conn.cursor()

    table_name = "Cars" if vehicle_type == "Car" else "Bikes"
    cursor.execute(f"UPDATE {table_name} SET availability = ? WHERE id = ?", (is_available, vehicle_id))
    
    conn.commit()
    conn.close()

def add_purchase(customer_name, customer_phone, vehicle_id, vehicle_type):
    conn = connect_to_db()
    cursor = conn.cursor()

    purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    cursor.execute('INSERT INTO Purchases (customer_name, customer_phone, vehicle_id, vehicle_type, purchase_date) VALUES (?, ?, ?, ?, ?)',
                   (customer_name, customer_phone, vehicle_id, vehicle_type, purchase_date))

    conn.commit()
    conn.close()


def drop_table():
    conn = connect_to_db()
    cursor = conn.cursor()

    choice = input("[1] Cars\n[2] Bikes\n[3] Customers\nWhat do you want delete : ").strip()
    
    if choice == '1':
        choice = 'Cars'
    elif choice == '2':
        choice = 'Bikes'
    elif choice == '3':
        choice = 'Purchases'
    else:
        print("invalid choice!")

    

    if input("Are you sure ?? [y/n] : ").strip().lower() == 'y':
        cursor.execute(f'DROP TABLE {choice}')

    print(f"Table {choice} Deleted successfully!")
    conn.commit()
    conn.close()

def drop_db():
    if input("Are you sure ?? [TYPE : yes] : ").strip().lower() == 'yes':
        os.remove('dealership.db')
    print("Data base dropped successfully!")

if __name__ == "__main__" :
    print("please open dealership_management_system.py")