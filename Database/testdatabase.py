fromfrom sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create the engine to connect to the database
engine = create_engine('postgresql://username:password@localhost/bungalowpark')

# Create a Session class for interacting with the database
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

# Create the declarative base for defining models
Base = declarative_base()

# Define the Bungalow model
class Bungalow(Base):
    __tablename__ = 'bungalows'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    bungalow_type = Column(Integer)
    capacity = Column(Integer)
    weekly_price = Column(Integer)

    def __repr__(self):
        return f"<Bungalow(id={self.id}, name='{self.name}', type={self.bungalow_type}, capacity={self.capacity}, weekly_price={self.weekly_price})>"

# Define the Guest model
class Guest(Base):
    __tablename__ = 'guests'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return f"<Guest(id={self.id}, username='{self.username}', password='{self.password}')>"

# Define the Booking model
class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    guest_id = Column(Integer, ForeignKey('guests.id'))
    bungalow_id = Column(Integer, ForeignKey('bungalows.id'))
    week = Column(Date)

    def __repr__(self):
        return f"<Booking(id={self.id}, guest_id={self.guest_id}, bungalow_id={self.bungalow_id}, week={self.week})>"

# Create the tables in the database
Base.metadata.create_all(engine)

# Insert some sample data
bungalow1 = Bungalow(name='Beach House', bungalow_type=8, capacity=8, weekly_price=1200)
session.add(bungalow1)

guest1 = Guest(username='johndoe', password='password')
session.add(guest1)

booking1 = Booking(guest_id=guest1.id, bungalow_id=bungalow1.id, week='2023-06-01')
session.add(booking1)

# Commit the changes to the database
session.commit()

# Query the database
bookings = session.query(Booking).all()
for booking in bookings:
    print(booking)
