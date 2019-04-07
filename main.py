from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema import Base, Sale
from insert import new_agent, new_office_with_agents, new_listing, new_sale
from seed import seed_data
from calculate import calculate

def reset_db(engine):
    Base.metadata.drop_all(bind=engine)   # reset database
    Base.metadata.create_all(bind=engine)   # create tables
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    print ("### Reseted Database ###")
    return session



def main():

    ### setup database ###
    engine = create_engine('sqlite:///real-estate.db', echo=False)
    session = reset_db(engine)


    ### insert some data ###
    # new agents
    new_agent(session, 'Maximillian', 'Choi', '(022)492-0928', 'm.choi@gmail.com')
    new_agent(session, 'Ewen', 'Rowland', '(934)120-3346', 'ewen@gmail.com')
    new_agent(session, 'Zahara', 'Mcgill', '(920)929-2704', 'zahara.zahara@hotmail.com')
    new_agent(session, 'Ishmael', 'Kaye', '(391)492-8289', 'ishmael.k@gmail.com')

    # office with agents
    new_office_with_agents(session, 'Big Apple', '1832 3rd Street', [1, 2, 4])

    # new listing
    new_listing(session, 3, 2, '291 Green Rd', '19382', 1043000, '2019-03-01', 2, 1)

    # new sale
    new_sale(session, 'Dolores', 'Gillispie', '(404)449-8679',
             'd.gillispie@gmail.com', 950000, '2019-03-19', 2, 1, 1)


    ### seed random data ###
    session = reset_db(engine)   # reset databese to remove existing data
    seed_data(session)

    ### Calculate Commission and Summary ###
    sales = session.query(Sale).all()
    for sale in sales:
        calculate(session, sale)
    print ("Commission and summary calculated")


if __name__ == '__main__':
    main()
