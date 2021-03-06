from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()
Session = sessionmaker()

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	email = Column(String(250), nullable = False)
	picture = Column(String(250), nullable = True)

class Restaurant(Base):
	__tablename__ = 'restaurant'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return {
			'name' : self.name,
			'id' : self.id
		}

class MenuItem(Base):
	__tablename__ = 'menu_item'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(
		Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)


	@property
	def serialize(self):
		#Returns object data in easily serializeable format
		return {
			'name'			: self.name,
			'description'	: self.description,
			'id'			: self.id,
			'price'			: self.price,
			'course'		: self.course,
		}


#######insert at end of file #######
engine = create_engine('postgresql://restaurantmenuwithusers')
if not database_exists(engine.url):
	create_database(engine.url)
Base.metadata.create_all(engine)
Session.configure(bind=engine)
session = Session()