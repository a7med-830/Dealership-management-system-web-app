# dealership_objects.py
from database import *
# from tabulate import tabulate
from flask import flash
class Vehicle:
    def __init__(self, brand, model, year, price, isAvailable):
        self.brand = brand 
        self.model = model
        self.year = year
        self.price = price
        self.isAvailable = isAvailable

    def get_info(self):
        print(f"Vehicle name: {self.brand} {self.model}")
        print(f"Year: {self.year}")
        print(f"Price: ${self.price}")
        print("Available for purchase" if self.isAvailable else "Sold")
        print("-" * 30)


    def buy(customer_name, customer_phone, vehicle_id, vehicle_type):
        conn = connect_to_db()
        cursor = conn.cursor()

        table_name = "Cars" if vehicle_type == "Car" else "Bikes"

        cursor.execute(f"SELECT availability FROM {table_name} WHERE id = ?", (vehicle_id,))
        result = cursor.fetchone()

        # if not result:
        #     print(f"{vehicle_type} with ID {vehicle_id} does not exist.")
        #     return
        
        is_available = result[0]
        if is_available == 'No':
            # print(f"{vehicle_type} with ID {vehicle_id} is not available for purchase.")
            flash(f"{vehicle_type} with ID {vehicle_id} is not available for purchase.", "failed")
            return

        update_vehicle_availability(vehicle_type, vehicle_id, "No")

        add_purchase_to_db(customer_name, customer_phone, vehicle_id, vehicle_type)

        flash(f"{vehicle_type} with ID {vehicle_id} has been purchased by {customer_name}.", "success")

    def return_(self):
        print(f"you have returned {self.brand} {self.model}")
        Cars.cars_num += 1
        self.isAvailable = False

class Cars(Vehicle):

    cars_num = 0

    def __init__(self, brand, model, year, form, price, isAvailable):
        super().__init__(brand, model, year, price , isAvailable)
        self.form = form
        Cars.cars_num += 1 
        
        
    @staticmethod
    def add_car():
        brand = input("Enter brand: ")
        model = input("Enter model: ")
        year = input("Enter year: ")
        form = input("Enter form: ")
        try:
            price = float(input("Enter price: "))
        except ValueError:
            print("invalid input!")
            
        new_car = Cars(brand, model, year, form, price, True)

        add_car_to_db(new_car)

        print("Car added successfully to the database!")

    @staticmethod
    def display_available_cars():
        print("Available Cars:")

        cars_from_db = fetch_all_cars()
        if not cars_from_db:
            print("No cars available in the database.")
            return

        # print(tabulate(cars_from_db, headers=["ID", "Brand", "Model", "Year", "Form", "Price", "Available"]))

    @staticmethod
    def cars_number():
        if Cars.cars_num == 1:
            print(f"We have 1 car available") 
        else:
            print(f"We have {Cars.cars_num} cars available")
   
    @staticmethod
    def delete_car():
        Cars.display_available_cars()
        id_num = input("Enter ID of the car you want to delete : ")
        delete_car_from_db(id_num)
        input("Press Enter to return to the menu.")
        
            

class Bikes(Vehicle):

    bikes_num = 0

    def __init__(self, brand, model, year, price, isAvailable):
        super().__init__(brand, model, year, price , isAvailable)
        Bikes.bikes_num += 1 
        
        
    @staticmethod
    def add_bike():
        brand = input("Enter brand: ")
        model = input("Enter model: ")
        year = input("Enter year: ")
        price = float(input("Enter price: "))
        
        new_bike = Bikes(brand, model, year, price, True)

        add_bike_to_db(new_bike)

        print("Bike added successfully to the database!")

    @staticmethod
    def display_available_bikes():
        print("Available Bikes:")

        bikes_from_db = fetch_all_bikes()
        if not bikes_from_db:
            print("No bikes available in the database.")
            return

        # print(tabulate(bikes_from_db, headers=["ID", "Brand", "Model", "Year", "Price", "Available"]))
    
    @staticmethod
    def bikes_number():
        if Bikes.bikes_num == 1:
            print(f"We have 1 bike available") 
        else:
            print(f"We have {Bikes.bikes_num} bikes available")

    @staticmethod
    def delete_bike():
        Bikes.display_available_bikes()
        id_num = input("Enter ID of the bike you want to delete : ")
        delete_bike_from_db(id_num)
        input("Press Enter to return to the menu.")

class Customer:


    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def add_purchase(self, vehicle_id, vehicle_type):
        Vehicle.buy(self.name, self.phone, vehicle_id, vehicle_type)

    def display_purchases(self):
        conn = connect_to_db()  
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM Purchases WHERE customer_name = ? AND customer_phone = ?', 
                        (self.name, self.phone))
            purchases = cursor.fetchall()

            # if purchases:
            #     print(f"{self.name}'s Purchases:")
            #     purchases = [row[3:] for row in purchases]
            #     print(tabulate(purchases, headers=["ID", "Type", "Date"]))
            # else:
            #     print(f"{self.name} has no recorded purchases.")

        except sqlite3.Error as e:
            flash(f"An error occurred while fetching purchases: {e}", "failed")
        
        finally:
            conn.close()

if __name__ == "__main__" :
    print("please open dealership_management_system.py")