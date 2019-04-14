import unittest
from sqlalchemy import create_engine

from  main import reset_db
from schema import Agent, Office
from insert import new_agent, new_office_with_agents, new_listing, new_sale


class InsertTestCase(unittest.TestCase):

    def test_insert_agent(self):

        ### bring up a new database ###
        engine = create_engine('sqlite:///real-estate-test.db', echo=False)
        session = reset_db(engine)

        new_agent(session, 'Maximillian', 'Choi', '(022)492-0928', 'm.choi@gmail.com')

        agent = session.query(Agent).filter_by(first_name='Maximillian',
                                               last_name='Choi',
                                               phone_number='(022)492-0928',
                                               email_address='m.choi@gmail.com').first()

        self.assertTrue(agent != None)


    def test_insert_office(self):

        ### bring up a new database ###
        engine = create_engine('sqlite:///real-estate-test.db', echo=False)
        session = reset_db(engine)

        new_agent(session, 'Maximillian', 'Choi', '(022)492-0928', 'm.choi@gmail.com')
        new_agent(session, 'Ewen', 'Rowland', '(934)120-3346', 'ewen@gmail.com')
        new_office_with_agents(session, 'Big Apple', '1832 3rd Street', [1, 2])

        office = session.query(Office).filter_by(name='Big Apple',
                                                 address='1832 3rd Street').first()
        self.assertTrue(office != None)
        self.assertTrue(office.agents[0].first_name == 'Maximillian')
        self.assertTrue(office.agents[1].first_name == 'Ewen')



if __name__ == '__main__':
    unittest.main()
