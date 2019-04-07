from faker import Faker
import random

from schema import *

def seed_data(session, num_of_agent=10, num_of_buyer=10, num_of_house=10):
    fake = Faker('en_US')

    # agent data
    for i in range(num_of_agent):
        agent = Agent(firest_name=fake.first_name(),
                      last_name=fake.last_name(),
                      phone_number=fake.phone_number(),
                      email_address=fake.email())
        session.add(agent)

    # buyer data
    for i in range(num_of_buyer):
        buyer = Buyer(firest_name=fake.first_name(),
                      last_name=fake.last_name(),
                      phone_number=fake.phone_number(),
                      email_address=fake.email())
        session.add(buyer)

    # house data
    for i in range(num_of_house):
        house = House(num_of_bedroom=random.randint(1,8),
                      num_of_bathroom=random.randint(1,6),
                      address=fake.street_address(),
                      zipcode=fake.postalcode())
        session.add(house)

    session.commit()
