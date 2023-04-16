import os
import bcrypt
import sqlite3
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, redirect, url_for, get_flashed_messages, flash
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, Mapper, session
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from wtforms import Form, SelectField, HiddenField, SubmitField, StringField
from wtforms.widgets import NumberInput
from flask import render_template, request

app = Flask(__name__)
app.secret_key = 'megasuperultrasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'bungalowpark.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# create an engine to connect to the database
engine = create_engine('sqlite:///bungalowpark.db')
Session = sessionmaker(bind=engine)

# define the metadata object
metadata = MetaData()

#define the users table
gebruikers_table = Table('gebruikers', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, unique=True),
    Column('password', String)
    )

# define the bungalows table
class Bungalow(db.Model):
    __tablename__ = 'bungalows'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    week_price = db.Column(db.Integer)


# define the guests table
guests = Table('guests', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('password', String)
)

# define the bookings table

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    bungalow_id = db.Column(db.Integer, db.ForeignKey('bungalows.id'))
    week = db.Column(db.Integer, unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    phone_number = db.Column(db.String(20))


class BookingForm(Form):
    first_name = StringField('Achternaam')
    last_name = StringField('Voornaam')
    email = StringField('Email')
    phone_number = StringField('Telefoonnummer', widget=NumberInput())
    week = SelectField('Week', choices=[(str(i), str(i)) for i in range(1, 53)])
    bungalow_id = HiddenField()
    submit = SubmitField('Boek')

# create the tables in the database
metadata.create_all(engine)


# app routes to all parts of the website
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session = Session()
        user = session.query(gebruikers_table).filter_by(username=username).first()
        if user and user.password == password:
            return render_template('index2.html')
        else:
            error = 'Gebruikersnaam of wachtwoord is onjuist.'
            flash('Gebruikersnaam of wachtwoord is onjuist!')
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/index2.html')
def index2():
    return render_template('index2.html')

@app.route('/contact2.html')
def contact2():
    return render_template('contact2.html')

# app routes to display database information


@app.route('/booking.html', methods=['GET', 'POST'])
def booking():
    bungalows_query = Bungalow.query.all()
    form = BookingForm(request.form)
    if request.method == 'POST' and form.validate():
        # get the bungalow ID and week from the form data
        bungalow_id = form.bungalow_id.data
        week = form.week.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        phone_number = form.phone_number.data
        
        # create a new booking object
        booking = Booking(
            bungalow_id=bungalow_id,
            week=week,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number
        )
        
        # add the booking to the session and commit it to the database
        db.session.add(booking)
        db.session.commit()
        
        # get the booked bungalow from the database
        bungalow = Bungalow.query.get(bungalow_id)
        
        # render the success template with booking details
        return render_template('success.html', bungalow=bungalow, week=week, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
    return render_template('booking.html', bungalows=bungalows_query, form=form)







# some code to make the website function properly


app.app_context().push()

if __name__ == '__main__':
    app.run(debug=True)


