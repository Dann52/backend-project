import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# sqlalchemy classes that coorespond to tables in our db
Base = declarative_base()

# add a user class to allow us to grant users authorization make changes
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class PlaceCategory(Base):
    # inside each class, must create table representation
    # we use __tablename__ to let sqlalchemy know
    # the variable we will use to refer to our table
    __tablename__ = 'place_category'
    # mapper code
    # specify name, that it's a string up to 80 chars, and not nullable
    name = Column(
        String(80), nullable=False)
    id = Column(
        Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # add the serialize function to return object for JSON data
        return {
            'name': self.name,
            'id': self.id
        }


class Place(Base):
    __tablename__ = 'place'
    # mapper code
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    category_id = Column(
        Integer, ForeignKey('place_category.id'))
    category = relationship(PlaceCategory)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price
        }


# configuration code at the end of the file #

# create instance of the create_engine class and point to the db
# creates a new db
engine = create_engine(
        'postgresql://catalog:catalog@localhost/catalog')


Base.metadata.create_all(engine)
