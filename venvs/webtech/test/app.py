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

app = Flask(__name__)
app.secret_key = 'megasuperultrasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'bungalows.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# create an engine to connect to the database
engine = create_engine('sqlite:///bungalowpark.db', echo=True)
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
bungalows = Table('bungalows', metadata, 
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('type', String),
    Column('size', Integer),
    Column('week_price', Integer)
)

# define the guests table
guests = Table('guests', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('password', String)
)

# define the bookings table
bookings = Table('bookings', metadata,
    Column('id', Integer, primary_key=True),
    Column('guest_id', Integer, ForeignKey('guests.id')),
    Column('bungalow_id', Integer, ForeignKey('bungalows.id')),
    Column('week', Integer)
)

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

@app.route('/booking.html')
def booking():
    return render_template('booking.html')

@app.route('/index2.html')
def index2():
    return render_template('index2.html')

@app.route('/contact2.html')
def contact2():
    return render_template('contact2.html')

@app.route('/booking2.html')
def booking2():
    return render_template('booking2.html')


app.app_context().push()

if __name__ == '__main__':
    app.run(debug=True)


