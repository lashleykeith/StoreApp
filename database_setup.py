# Setting up the database
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))

class Store(Base):
	__tablename__ = 'store'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
	inventory_item = relationship('InventoryItem', cascade='all, delete-orphan')


	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'name'			: self.name,
			'id'			: self.id,
		}

class InventoryItem(Base):
	__tablename__ = 'inventory_item'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	description = Column(String(250))
	price = Column(String(8))
	course = Column(String(250))
	store_id = Column(Integer, ForeignKey('store.id'))
	store = relationship('Store')
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		"""Return object data in easily serializable format"""
		return {
			'name'			: self.name,
			'description'	: self.description,
			'id'			: self.id,
			'price'			: self.price,
			'course'		: self.course,
		}

engine = create_engine('sqlite:///storeinventorywithusers.db')

Base.metadata.create_all(engine)