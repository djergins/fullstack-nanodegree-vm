from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy
from dateutil.relativedelta import relativedelta
from datetime import date

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def getPuppies():
	for instance in session.query(Puppy).order_by(Puppy.name):
		print(instance.name, instance.gender, 
			  instance.dateOfBirth, instance.shelter_id,
			  instance.weight)
	

def getYoungPuppies():
	today = date.today()
	six_months_past = today - relativedelta(months=6)
	for instance in session.query(Puppy)\
	.filter(Puppy.dateOfBirth >= six_months_past)\
	.order_by(Puppy.dateOfBirth):
		print(instance.name, instance.gender, 
			  instance.dateOfBirth, instance.shelter_id,
			  instance.weight)

def getPuppiesByWeight():
	for instance in session.query(Puppy).order_by(Puppy.weight):
		print(instance.name, instance.gender, 
			  instance.dateOfBirth, instance.shelter_id,
			  instance.weight)

def getPuppiesByShelter():
	for instance in session.query(Puppy).order_by(Puppy.shelter_id):
		print(instance.name, instance.gender, 
			  instance.dateOfBirth, instance.shelter_id,
			  instance.weight)

def addPuppyToShelter(puppyName, puppyGender, puppyShelter):
	session.add(Puppy(name = puppyName, gender = puppyGender, 
		shelter_id = puppyShelter)) 

def addShelter(shelterName, shelterCapacity):
	session.add(Shelter(name= shelterName, maximumCapacity = shelterCapacity))

def getShelter():
	for instance in session.query(Shelter).order_by(Shelter.id):
		print(instance.id, instance.name)

def getCurrentShelterPopulation():
	'''TODO 
	Counting

Query includes a convenience method for counting called count():

SQL>>> session.query(User).filter(User.name.like('%ed')).count()
2'''




if __name__ == '__main__':
	getPuppies()
	getYoungPuppies()
	getPuppiesByWeight()
	getPuppiesByShelter()
	#addPuppyToShelter("Thor", "M", 6)
	addShelter("Awesome Shelter for a Puppy", 1)
	getShelter()
	