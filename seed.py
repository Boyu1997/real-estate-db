from faker import Faker
import random

from schema import Agent, Office, Buyer, House, Listing

def seed_data(session, num_of_agent=50, num_of_office=10,
              num_of_buyer=100, num_of_house=100, num_of_listing=105):
    fake = Faker('en_US')

    for i in range(num_of_agent):
        agent = Agent(firest_name=fake.first_name(),
                      last_name=fake.last_name(),
                      phone_number=fake.phone_number(),
                      email_address=fake.email())
        session.add(agent)
    session.commit()

    for i in range(num_of_office):
        agent_ids = random.sample(range(1, num_of_agent+1), random.randint(1, min(20, num_of_agent)))
        agents = [session.query(Agent).get(id) for id in agent_ids]
        office = Office(name=fake.color_name(),
                        address=fake.street_address(),
                        agents=agents)
        session.add(office)
    session.commit()

    for i in range(num_of_buyer):
        buyer = Buyer(firest_name=fake.first_name(),
                      last_name=fake.last_name(),
                      phone_number=fake.phone_number(),
                      email_address=fake.email())
        session.add(buyer)

    for i in range(num_of_house):
        house = House(num_of_bedroom=random.randint(1,8),
                      num_of_bathroom=random.randint(1,6),
                      address=fake.street_address(),
                      zipcode=fake.postalcode())
        session.add(house)

    for i in range(num_of_listing):
        listing = Listing(listing_price=random.randint(10000,100000000),
                          date_of_listing=fake.date_between(start_date="-90d", end_date="today"),
                          house=house)
        session.add(listing)

    session.commit()
