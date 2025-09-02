from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
DATABASE_URL = "sqlite:///./Restaurent.db"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True)
    table_number = Column(Integer, unique=True, nullable=False)
    seats = Column(Integer, nullable=False)

class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    table_number = Column(Integer, nullable=False)
    reservation_date = Column(String, nullable=False)

Base.metadata.create_all(engine)

def Add_User(name, email, password):
    user = session.query(User).filter_by(email=email).first()
    if user:
        return False
    new_user = User(name=name, email=email, password=password)
    session.add(new_user)
    session.commit()
    return True
def Check_User(name, password):
    user = session.query(User).filter_by(name=name, password=password).first()
    if user:
        return True
    return False

def Get_id(name, password):
    user = session.query(User).filter_by(name=name, password=password).first()
    if user:
        return user.id
    return None




def Get_All_Tables():
    return session.query(Table).order_by(Table.table_number).all()

def Make_Tables(num:int):
    num_existing_tables = session.query(Table).count()
    if num_existing_tables >= 1:
        return
    for i in range(1, num + 1):
        table = Table(table_number=i, seats=4)
        session.add(table)
    session.commit()

from datetime import date, timedelta




def make_reservation(user_id, table_number, reservation_date):
    reservation = Reservation(user_id=user_id, table_number=table_number, reservation_date=reservation_date)
    session.add(reservation)
    session.commit()
    return True

def Get_Available_Tables(reservation_date):
    booked_tables = session.query(Reservation.table_number).filter_by(reservation_date=reservation_date).all()
    booked_table_numbers = {table[0] for table in booked_tables}
    all_tables = session.query(Table).all()
    available_tables = [table for table in all_tables if table.table_number not in booked_table_numbers]
    return available_tables

def Get_All_Tables():
    return session.query(Table).all()

def Get_user_reservations(user_id):
    return session.query(Reservation).filter_by(user_id=user_id).all()

def Cancel_Reservation(reservation_id):
    reservation = session.query(Reservation).filter_by(id=reservation_id).first()
    if reservation:
        session.delete(reservation)
        session.commit()
        return True
    return False