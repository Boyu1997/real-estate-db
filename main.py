from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from schema import Base

engine = create_engine('sqlite:///real-estate.db', echo=True)
Base.metadata.create_all(bind=engine)
