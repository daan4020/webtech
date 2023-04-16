import os
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
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
    Column('password_hash', String)
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

# @app.route('/')
# def index():
#     session = Session()
#     bungalows_list = session.query(bungalows).all()
#     return render_template('index.html', bungalows=bungalows_list)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            return redirect(url_for('dashboard'))
        else:
            error = 'Gebruikersnaam of wachtwoord is onjuist.'
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


app.app_context().push()

if __name__ == '__main__':
    app.run(debug=True)


