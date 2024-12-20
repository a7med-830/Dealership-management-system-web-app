from flask import Flask, render_template

app = Flask(__name__)

from database import *

my_cars = fetch_all_cars()
my_bikes = fetch_all_bikes()



@app.route('/')
def homepage():
    return render_template('index.html', 
                           title = "Home Page", 
                           page_head="Dealership Management System")


@app.route('/manger')
def manger():
    return render_template("manger.html", 
                           title = "manger Menu", 
                           custom_css = "manger.css",
                           page_head = "Manger Menu")

@app.route("/buy")
def buy():
    return render_template("buy.html",
                           title = "Buy menu",
                           custom_css = "buy.css",
                           page_head = "Buy a new car",
                           cars = my_cars,
                           bikes = my_bikes)


@app.route("/view")
def view():
    return render_template("view.html",
                           title = "view menu",
                           custom_css = "view.css",
                           page_head = "Available vehicles",
                           cars = my_cars,
                           bikes = my_bikes)

@app.route("/login")
def login():
    return render_template("login.html",
                           title = "Login",
                           page_head = "Manger Login")    

if __name__ == '__main__':
    app.run(debug=True)