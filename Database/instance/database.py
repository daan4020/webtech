import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()

    
class Bungalow(db.Model):
    __tablename__ = 'bungalows'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    bungalow_type = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    weekly_price = db.Column(db.Integer)

    def __repr__(self):
        return f"<Bungalow(id={self.id}, name='{self.name}', type={self.bungalow_type}, capacity={self.capacity}, weekly_price={self.weekly_price})>"

class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<Guest(id={self.id}, username='{self.username}', password='{self.password}')>"
    
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, ForeignKey('guests.id'))
    bungalow_id = db.Column(db.Integer, ForeignKey('bungalows.id'))
    week = db.Column(db.Date)

    def __repr__(self):
        return f"<Booking(id={self.id}, guest_id={self.guest_id}, bungalow_id={self.bungalow_id}, week={self.week})>"
    
