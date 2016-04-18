from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy, PuppyAdopterLink
from dateutil.relativedelta import relativedelta
from datetime import date
from ShelterQuery import *

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

def addPuppyToShelter(puppyName, puppyGender, puppyShelter = None,
	puppyPicture = None, puppyDOB = None, puppyAdopter = None, 
	puppyWeight = None):
	if puppyShelter:
		enrollment_flag = False
		while enrollment_flag == False:
			shelter_population = getShelterCurrentPopulation(puppyShelter)
			max_capacity = getShelterMaxOccupancy(puppyShelter)
			print "Printing the population boss."
			print shelter_population
			print "Printing the max capacity boss."
			print max_capacity
			if shelter_population == max_capacity:
				if getVacantShelters() == 0:
					print "We are sorry, all shelters are full. A new shelter must be constructed."
					enrollment_flag = True
				print "Shelter is currently full, please select another shelter."
				puppyShelter = getShelterWithLowestPopulation()
				print puppyShelter
				enrollment_flag = False
			else:
				print "Adding the puppy boss."
				print puppyShelter
				puppy = Puppy(name = puppyName, gender = puppyGender,
					shelter_id = puppyShelter, picture = puppyPicture,
					dateOfBirth = puppyDOB, 
					weight = puppyWeight)
				session.add(puppy) 
				session.commit()
				enrollment_flag = True
	else:
		print "Adding the puppy without a shelter boss."
		puppy = Puppy(name = puppyName, gender = puppyGender,
			shelter_id = puppyShelter, picture = puppyPicture,
			dateOfBirth = puppyDOB, 
			weight = puppyWeight)
		session.add(puppy) 
		session.commit()

def adoptPuppy(puppyID, *puppyAdopters):
	print "Removing the puppy from the shelter"
	session.query(Puppy).filter(Puppy.id == puppyID).\
	update({Puppy.shelter_id: None})
	session.commit()
	for adopter in puppyAdopters:
		adoption = PuppyAdopterLink(puppy_id = puppyID, adopter_id = adopter)
		session.add(adoption)
		session.commit()


if __name__ == '__main__':
# 	getPuppies()
# 	getYoungPuppies()
# 	getPuppiesByWeight()
# 	getPuppiesByShelter()
 	addPuppyToShelter("Thor", "M", 1)
# 	addShelter("Awesome Shelter for a Puppy", 1)
# 	getShelter()
	