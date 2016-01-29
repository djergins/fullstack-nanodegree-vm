import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
	__tablename__ = 'shelter'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable = False)
	address = Column(String(50), nullable = False)
	city = Column(String(30), nullable=False)
	zipCode = Column(Integer, nullable=False)
	website = Column(String(200))


class Puppy(Base):
	__tablename__ = 'puppy'
	name = Column(String(50), nullable = False)
	dateOfBirth = Column(String(15), nullable = False)
	gender = Column(String(1), nullable = False)
	weight = Column(String(8), nullable = False)
	shelterId = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)

engine = create_engine('sqlite:///shelter.db')
Base.metadata.create_all(engine)
