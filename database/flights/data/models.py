from sqlalchemy import Column, Integer, SmallInteger, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Carrier(Base):
    __tablename__ = 'carrier'
    id = Column(Integer, primary_key=True)
    code = Column(String(8), unique=True, nullable=False)  # UNIQUE_CARRIER
    airline_id = Column(Integer, unique=True, nullable=False)  # AIRLINE_ID
    flights = relationship('Flight', back_populates='carrier')

class Airport(Base):
    __tablename__ = 'airport'
    id = Column(Integer, primary_key=True)
    code = Column(String(8), unique=True, nullable=False)  # ORIGIN or DEST
    flights_origin = relationship('Flight', back_populates='origin', foreign_keys='Flight.origin_id')
    flights_dest = relationship('Flight', back_populates='dest', foreign_keys='Flight.dest_id')

class TimeBlock(Base):
    __tablename__ = 'time_block'
    id = Column(Integer, primary_key=True)
    block = Column(String(16), unique=True, nullable=False)  # DEP_TIME_BLK, ARR_TIME_BLK
    flights_dep = relationship('Flight', back_populates='dep_time_blk', foreign_keys='Flight.dep_time_blk_id')
    flights_arr = relationship('Flight', back_populates='arr_time_blk', foreign_keys='Flight.arr_time_blk_id')

class Flight(Base):
    __tablename__ = 'flight'
    id = Column(Integer, primary_key=True)
    flight_date = Column(Date, nullable=False)  # FL_DATE
    day_of_week = Column(SmallInteger, nullable=False)  # DAY_OF_WEEK
    flight_number = Column(Integer, nullable=False)  # FL_NUM

    carrier_id = Column(Integer, ForeignKey('carrier.id'), nullable=False)
    origin_id = Column(Integer, ForeignKey('airport.id'), nullable=False)
    dest_id = Column(Integer, ForeignKey('airport.id'), nullable=False)
    dep_time_blk_id = Column(Integer, ForeignKey('time_block.id'))
    arr_time_blk_id = Column(Integer, ForeignKey('time_block.id'))

    crs_dep_time = Column(String(4))  # CRS_DEP_TIME
    dep_time = Column(String(4))  # DEP_TIME
    dep_delay = Column(Float)
    dep_delay_new = Column(Float)
    dep_del15 = Column(Boolean)
    dep_delay_group = Column(SmallInteger)
    taxi_out = Column(Float)
    wheels_off = Column(String(4))
    wheels_on = Column(String(4))
    taxi_in = Column(Float)
    crs_arr_time = Column(String(4))
    arr_time = Column(String(4))
    arr_delay = Column(Float)
    arr_delay_new = Column(Float)
    arr_del15 = Column(Boolean)
    arr_delay_group = Column(SmallInteger)

    cancelled = Column(Boolean)
    cancellation_code = Column(String(1))
    diverted = Column(Boolean)

    crs_elapsed_time = Column(Float)
    actual_elapsed_time = Column(Float)
    air_time = Column(Float)

    # Relationships
    carrier = relationship('Carrier', back_populates='flights')
    origin = relationship('Airport', back_populates='flights_origin', foreign_keys=[origin_id])
    dest = relationship('Airport', back_populates='flights_dest', foreign_keys=[dest_id])
    dep_time_blk = relationship('TimeBlock', back_populates='flights_dep', foreign_keys=[dep_time_blk_id])
    arr_time_blk = relationship('TimeBlock', back_populates='flights_arr', foreign_keys=[arr_time_blk_id])
