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

def getCurrentSheltersPopulation():
	shelters = []
	for instance in session.query(Shelter):
		shelters.append(instance.shelter_count)
	return shelters


def getHighestShelterPopulation():
	shelters = getCurrentSheltersPopulation()
	maxShelter = max(shelters)
	print maxShelter
	return maxShelter

def getLowestPopulationShelter():
	shelters = getCurrentSheltersPopulation()
	minShelter = min(shelters)
	return minShelter

def getShelterWithLowestPopulation():
	lowestPopulation = getLowestPopulationShelter()
	for instance in session.query(Shelter).filter(Shelter.shelter_count == lowestPopulation):
		return instance.id
	

def getShelterCurrentPopulation(puppyShelter = None):
	for instance in session.query(Shelter).filter(Shelter.id == puppyShelter):
		shelter_count = instance.shelter_count
	return shelter_count

def getShelterMaxOccupancy(puppyShelter):
	for instance in session.query(Shelter).filter(Shelter.id == puppyShelter):
		max_capacity = instance.maximumCapacity
	return max_capacity

def setShelterMaxOccupancy(shelterId, shelterMaxOccupancy):
	session.query(Shelter).filter(Shelter.id == shelterId).\
		update({Shelter.maximumCapacity: shelterMaxOccupancy},
			synchronize_session = False)
	session.commit()

def getVacantShelters():
	shelters = []
	for instance in session.query(Shelter).\
	filter(Shelter.shelter_count < Shelter.maximumCapacity):
		shelters.append(instance.name)
	print shelters
	print len(shelters)
	return len(shelters)

