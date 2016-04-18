from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy import create_engine, func
from sqlalchemy_utils import aggregated
 
Base = declarative_base()
Session = sessionmaker()

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    maximumCapacity = Column(Integer)
    @aggregated('puppies', Column(Integer))
    def shelter_count(self):
        return func.count(Puppy.id)
    puppies = relationship("Puppy")

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship("Shelter")
    adopter = relationship("Adopter", secondary = 'puppy_adopter_link')
    weight = Column(Numeric(10))

class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    puppy = relationship("Puppy", secondary = 'puppy_adopter_link')


class PuppyProfile(Base):
    __tablename__ = 'puppy_profile'
    id = Column(Integer, primary_key = True)
    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    picture = Column(String)
    description = Column(String)
    special_needs = Column(String)
    puppy = relationship(Puppy)

class PuppyAdopterLink(Base):
    __tablename__ = 'puppy_adopter_link'
    puppy_id = Column(Integer, ForeignKey('puppy.id'), primary_key = True)
    adopter_id = Column(Integer, ForeignKey('adopter.id'), primary_key = True)
    puppy = relationship(Puppy, backref=backref("adopter_assoc"))
    adopter = relationship(Adopter, backref=backref("puppy_assoc"))

engine = create_engine('sqlite:///puppyshelter.db') 
Base.metadata.create_all(engine)
Session.configure(bind=engine)
session = Session()
