from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy
from dateutil.relativedelta import relativedelta
from datetime import date

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def addShelter(shelterName, shelterAddress,
	shelterCity, shelterState, shelterZip, 
	shelterWebsite, shelterMaxCapacity, shelterOccupancy):
	session.add(Shelter(name= shelterName,
		address = shelterAddress, city = shelterCity,
		state = shelterState, zipCode = shelterZip, 
		website = shelterWebsite, maximumCapacity = shelterCapacity,
		currentOccupancy = shelterOccupancy))

def getShelter():
	for instance in session.query(Shelter).order_by(Shelter.id):
		print(instance.id, instance.name)

def getCurrentShelterPopulation():
	shelters = []
	i = 0
	for instance in session.query(func.count(Puppy.id)).\
	group_by(Puppy.shelter_id):
		shelters.append(instance)
	return shelters

def getHighestShelterPopulation():
	shelters = getCurrentShelterPopulation()
	maxShelter = max(shelters)
	print maxShelter
	return shelters

def getLowestPopulationShelter():
	shelters = getCurrentShelterPopulation()
	minShelter = min(shelters)
	print minShelter
	return shelters

def setShelterMaxOccupancy(shelterId, shelterMaxOccupancy):
	session.query(Shelter).filter(Shelter.id == shelterId).\
		update({Shelter.maximumCapacity: shelterMaxOccupancy},
			synchronize_session = False)
	session.commit()
