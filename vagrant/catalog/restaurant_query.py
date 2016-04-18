from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def getRestaurants():
	output = ""
	for instance in session.query(Restaurant).all():
		output+= instance.name
		output+= "<a href= '#' >Edit</a>"
		output+= "<a href= '#' >Delete</a>"
		output+= "</br>"
	return output

if __name__ == '__main__':
	getRestaurants()