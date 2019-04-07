from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, ForeignKey, Integer, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

agent_office = Table('AgentOffice', Base.metadata,
    Column('agent_id', Integer, ForeignKey('Agent.id')),
    Column('office_id', Integer, ForeignKey('Office.id'))
)


class Agent(Base):
    __tablename__ = 'Agent'
    id = Column('id', Integer, primary_key=True)

    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    phone_number = Column('phone_number', String)
    email_address = Column('email_address', String)

    offices = relationship('Office', secondary=agent_office, back_populates='agents')


class Office(Base):
    __tablename__ = 'Office'
    id = Column('id', Integer, primary_key=True)

    name = Column('name', String)
    address = Column('address', String)

    agents = relationship('Agent', secondary=agent_office, back_populates='offices')


class House(Base):
    __tablename__ = 'House'
    id = Column('id', Integer, primary_key=True)

    num_of_bedroom = Column('num_of_bedroom', Integer)
    num_of_bathroom = Column('num_of_bathroom', Integer)
    address = Column('address', String)
    zipcode = Column('zipcode', String)


class Listing(Base):
    __tablename__ = 'Listing'
    id = Column('id', Integer, primary_key=True)

    listing_price = Column('listing_price', Integer)
    date_of_listing = Column('date_of_listing', String)
    status = Column('status', String)

    agent_id = Column(Integer, ForeignKey('Agent.id'))
    agent = relationship(Agent)
    office_id = Column(Integer, ForeignKey('Office.id'))
    office = relationship(Office)
    house_id = Column(Integer, ForeignKey('House.id'))
    house = relationship(House)


class Buyer(Base):
    __tablename__ = 'Buyer'
    id = Column('id', Integer, primary_key=True)

    first_name = Column('first_name', String)
    last_name = Column('last_name', String)
    phone_number = Column('phone_number', String)
    email_address = Column('email_address', String)


class Sale(Base):
    __tablename__ = 'Sale'
    id = Column('id', Integer, primary_key=True)

    sale_price = Column('sale_price', Integer)
    date_of_sale = Column('date_of_sale', String)

    listing_id = Column(Integer, ForeignKey('Listing.id'))
    listing = relationship(Listing)
    buyer_id = Column(Integer, ForeignKey('Buyer.id'))
    buyer = relationship(Buyer)
    agent_id = Column(Integer, ForeignKey('Agent.id'))
    agent = relationship(Agent)
    office_id = Column(Integer, ForeignKey('Office.id'))
    office = relationship(Office)


class Cycle(Base):
    __tablename__ = 'Cycle'
    id = Column('id', Integer, primary_key=True)

    year = Column('year', Integer)
    month = Column('month', Integer)


class AgentCommission(Base):
    __tablename__ = 'AgentCommission'
    id = Column('id', Integer, primary_key=True)

    commission_amount = Column('commission_amount', Integer)

    agent_id = Column(Integer, ForeignKey('Agent.id'))
    agent = relationship(Agent)
    cycle_id = Column(Integer, ForeignKey('Cycle.id'))
    cycle = relationship(Cycle)


class AgentSummary(Base):
    __tablename__ = 'AgentSummary'
    id = Column('id', Integer, primary_key=True)

    total_sale = Column('total_sale', Integer)

    agent_id = Column(Integer, ForeignKey('Agent.id'))
    agent = relationship(Agent)
    cycle_id = Column(Integer, ForeignKey('Cycle.id'))
    cycle = relationship(Cycle)


class OfficeSummary(Base):
    __tablename__ = 'OfficeSummary'
    id = Column('id', Integer, primary_key=True)

    total_sale = Column('total_sale', Integer)

    office_id = Column(Integer, ForeignKey('Office.id'))
    office = relationship(Office)
    cycle_id = Column(Integer, ForeignKey('Cycle.id'))
    cycle = relationship(Cycle)
