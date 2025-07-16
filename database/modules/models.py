from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Workclass(Base):
    __tablename__ = 'workclass'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    persons = relationship('Person', back_populates='workclass')

class Education(Base):
    __tablename__ = 'education'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    persons = relationship('Person', back_populates='education')

class MaritalStatus(Base):
    __tablename__ = 'marital_status'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    persons = relationship('Person', back_populates='marital_status')

class Occupation(Base):
    __tablename__ = 'occupation'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    persons = relationship('Person', back_populates='occupation')

class NativeCountry(Base):
    __tablename__ = 'native_country'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    persons = relationship('Person', back_populates='native_country')

class ClassLabel(Base):
    __tablename__ = 'class_label'
    id = Column(Integer, primary_key=True)
    name = Column(String(8), unique=True, nullable=False)
    persons = relationship('Person', back_populates='class_label')

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    workclass_id = Column(Integer, ForeignKey('workclass.id'))
    education_id = Column(Integer, ForeignKey('education.id'))
    marital_status_id = Column(Integer, ForeignKey('marital_status.id'))
    occupation_id = Column(Integer, ForeignKey('occupation.id'))
    capital_gain = Column(Integer)
    capital_loss = Column(Integer)
    hours_per_week = Column(Integer)
    native_country_id = Column(Integer, ForeignKey('native_country.id'))
    class_label_id = Column(Integer, ForeignKey('class_label.id'))

    workclass = relationship('Workclass', back_populates='persons')
    education = relationship('Education', back_populates='persons')
    marital_status = relationship('MaritalStatus', back_populates='persons')
    occupation = relationship('Occupation', back_populates='persons')
    native_country = relationship('NativeCountry', back_populates='persons')
    class_label = relationship('ClassLabel', back_populates='persons')