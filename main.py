from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import Base
from seed import seed_data

engine = create_engine('sqlite:///real-estate.db', echo=False)
Base.metadata.create_all(bind=engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

seed_data(session)
