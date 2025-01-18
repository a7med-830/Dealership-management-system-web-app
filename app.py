from flask import Flask, render_template, flash, redirect, url_for
from database import *
from forms import *
from dealership_objects import *
my_cars = fetch_all_cars()
my_bikes = fetch_all_bikes()
app = Flask(__name__)
app.config['SECRET_KEY'] = "5cb8fba25e3022ce32f7b9ad0c0781bd"

if not os.path.exists('dealership.db'):
    initialize_database()

@app.route('/')
def homepage():
    return render_template('index.html', 
                           title = "Home Page", 
                           page_head="Dealership Management System")


@app.route('/manager')
def manager():
    return render_template("manager.html", 
                           title = "manager Menu", 
                           custom_css = "manager.css",
                           page_head = "Manager Menu")

@app.route("/buy", methods=['GET', 'POST'])
def buy():
    buy_form = BuyForm()
    car_name = [f"{car[1]} {car[2]}" for car in my_cars]
    bike_name = [f"{bike[1]} {bike[2]}" for bike in my_bikes]
    
    
    try:
        if buy_form.validate_on_submit():
            availability = check_availability(buy_form.vehicle_id.data, buy_form.vehicle_type.data)
            if availability == 'Yes':
                customer = Customer(buy_form.customer_name.data, buy_form.phone.data)
                customer.add_purchase(buy_form.vehicle_id.data, buy_form.vehicle_type.data)
                
                if buy_form.vehicle_type.data == "Car":
                    flash(f"You have bought a {car_name[buy_form.vehicle_id.data -1]}", "success")
                elif buy_form.vehicle_type.data == "Bike":
                    flash(f"You have bought a {bike_name[buy_form.vehicle_id.data -1]}", "success")
                return redirect(url_for('homepage'))
    except IndexError:
        flash("Wrong vehicle ID or This Vehicle is not available", "failed")
            
            
    return render_template("buy.html",
                           title = "Buy menu",
                           custom_css = "buy.css",
                           page_head = "Buy a new car",
                           cars = my_cars,
                           bikes = my_bikes,
                           form = buy_form)


@app.route("/view")
def view():
    return render_template("view.html",
                           title = "view menu",
                           custom_css = "view.css",
                           page_head = "Available vehicles",
                           cars = my_cars,
                           bikes = my_bikes)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.password.data == "123123":
            flash("you have successfully logged in", "success")
            return redirect(url_for('manager'))
        else:
            flash("login unsuccessful", "failed")
    return render_template("login.html",
                           title = "Login",
                           page_head = "Manager Login",
                           form = login_form)    
    
@app.route("/add", methods=['GET','POST'])
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        if add_form.type.data == 'Car':
            car = Cars(add_form.brand.data, add_form.model.data, 
                       int(add_form.year.data), add_form.form.data,
                       float(add_form.price.data), True)
            add_car_to_db(car)
            flash("Car has been added to the database!", "success")
        elif add_form.type.data == 'Bike':
            bike = Bikes(add_form.brand.data, add_form.model.data, 
                       int(add_form.year.data), float(add_form.price.data), True)
            add_bike_to_db(bike)
            flash("Bike has been added to the database!", "success")
    else:
        for field, errors in add_form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(add_form, field).label.text}: {error}", "failed")
                        
    return render_template("add.html",
                           custom_css = "add.css",
                           page_head = "Add a New Vehicle",
                           form = add_form)

    

if __name__ == '__main__':
    app.run(debug=True)
