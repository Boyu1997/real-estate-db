from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import Base
from seed import seed_data

def main():
    # setup database
    engine = create_engine('sqlite:///real-estate.db', echo=False)
    Base.metadata.drop_all(bind=engine)   # reset database
    Base.metadata.create_all(bind=engine)   # create tables

    # seed 
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    seed_data(session)


if __name__ == '__main__':
    main()
