from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Optional

class BuyForm(FlaskForm):
    customer_name = StringField("Customer Name",
                                validators=[DataRequired(), Length(min=2)])
    
    phone = StringField("Phone",
                        validators=[DataRequired()])
    
    vehicle_type = RadioField("Type:",
                              choices=['Car', 'Bike'])
    
    vehicle_id = IntegerField("VehicleID")
    
    submit = SubmitField("Buy")
    
class LoginForm(FlaskForm):
    password = StringField("Manger password",
                           validators=[DataRequired()])
    
class AddForm(FlaskForm):
    type = RadioField("Type", validators=[DataRequired()],
                      choices=['Car', 'Bike'])
    brand = StringField("Brand", validators=[DataRequired()])
    model = StringField("Model", validators=[DataRequired()])
    year = IntegerField("Year", validators=[DataRequired()])
    form = RadioField("Form(cars only)",validators=[Optional()],
                      choices=['sedan', 'coupe', 'hatchback'])
    price = FloatField("Price", validators=[DataRequired()])
    
    submit = SubmitField("Add")