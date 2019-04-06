from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class Agent(Base):
    __tablename__ = 'Agent'
    id = Column('id', Integer, primary_key=True)

    firest_name = Column('firest_name', String)
    last_name = Column('last_name', String)

class Office(Base):
    __tablename__ = 'Office'
    id = Column('id', Integer, primary_key=True)

    name = Column('name', String)
    address = Column('address', String)

class AgentOffice(Base):
    __tablename__ = 'AgentOffice'
    id = Column('id', Integer, primary_key=True)

    agent_id = Column(Integer, ForeignKey('Agent.id'))
    agent = relationship(Agent)
    office_id = Column(Integer, ForeignKey('Office.id'))
    office = relationship(Office)


class Listing(Base):
    __tablename__ = 'Listing'
    id = Column('id', Integer, primary_key=True)

    listing_price = Column('listing_price', Numeric)
    date_of_listing = Column('date_of_listing', String)
    sold = Column('sold', Boolean)

    agent_id = Column(Integer, ForeignKey('Agent.id'))
    agent = relationship(Agent)


class House(Base):
    __tablename__ = 'House'
    id = Column('id', Integer, primary_key=True)

    num_of_bedroom = Column('num_of_bedroom', Integer)
    num_of_bathroom = Column('num_of_bathroom', Integer)
    zipcode = Column('zipcode', Integer)


class Buyer(Base):
    __tablename__ = 'Buyer'
    id = Column('id', Integer, primary_key=True)

    firest_name = Column('firest_name', String)
    last_name = Column('last_name', String)


class Sale(Base):
    __tablename__ = 'Sale'
    id = Column('id', Integer, primary_key=True)

    sale_price = Column('sale_price', Numeric)
    date_of_sale = Column('date_of_sale', String)

    listing_id = Column(Integer, ForeignKey('Listing.id'))
    listing = relationship(Listing)
    agent_id = Column(Integer, ForeignKey('Agent.id'))
    agent = relationship(Agent)


engine = create_engine('sqlite:///real-estate.db', echo=True)
Base.metadata.create_all(bind=engine)
