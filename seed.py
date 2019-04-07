from faker import Faker
import random
from datetime import datetime, timedelta

from schema import Agent, Office, Buyer, House, Listing, Sale

def seed_data(session, num_of_agent=30, num_of_office=10, num_of_buyer=300,
              num_of_house=500, num_of_listing=300, num_of_sale=200):

    fake = Faker('en_US')


    # create random agent
    for i in range(num_of_agent):
        agent = Agent(first_name=fake.first_name(),
                      last_name=fake.last_name(),
                      phone_number=fake.phone_number(),
                      email_address=fake.email())
        session.add(agent)
    session.commit()


    # create random offices
    # add many to many relationship between offices and agents
    for i in range(num_of_office):
        agent_ids = random.sample(range(1, num_of_agent+1), random.randint(1, min(30, num_of_agent)))
        agents = [session.query(Agent).get(id) for id in agent_ids]
        office = Office(name=fake.color_name(),
                        address=fake.street_address(),
                        agents=agents)
        session.add(office)
    session.commit()


    # create random buyers
    for i in range(num_of_buyer):
        buyer = Buyer(first_name=fake.first_name(),
                      last_name=fake.last_name(),
                      phone_number=fake.phone_number(),
                      email_address=fake.email())
        session.add(buyer)
    session.commit()


    # create random houses
    for i in range(num_of_house):
        house = House(num_of_bedroom=random.randint(1,8),
                      num_of_bathroom=random.randint(1,6),
                      address=fake.street_address(),
                      zipcode=fake.postalcode())
        session.add(house)
    session.commit()


    # create random listings
    # connect agent, office, and house with listing
    house_ids = random.sample(range(1, num_of_house+1), num_of_listing)
    for house_id in house_ids:
        office = session.query(Office).get(random.randint(1,num_of_office))
        agent = random.choice(office.agents)
        listing = Listing(listing_price=1000*random.randint(10,5000),
                          date_of_listing=fake.date_between(start_date='-1y', end_date='today'),
                          status='available',
                          agent=agent,
                          office=office,
                          house=session.query(House).get(house_id))
        session.add(listing)
    session.commit()


    # create random sales
    # connect agent, office, and listing with sale
    listing_ids = random.sample(range(1, num_of_listing+1), num_of_sale)
    for listing_id in listing_ids:
        listing = session.query(Listing).get(listing_id)
        listing.status = 'sold'

        # different situations of how the transition between listing and sale happens
        # the logic leaky as the next random choice may be the same as the last one
        # however this is acceptable as we are only to seed some example data
        if random.random() < 0.6:   # same agent in the same office made the sale
            agent = listing.agent
            office = listing.office
        elif random.random() < 0.9:   # different agent in the same office made the sale
            office = listing.office
            agent = random.choice(office.agents)
        else:   # different agent in a different officen made the sale
            office = session.query(Office).get(random.randint(1,num_of_office))
            agent = random.choice(office.agents)

        # calculate sale date bese on listing date
        listing_datetime = datetime.strptime(listing.date_of_listing, '%Y-%m-%d')
        days_variant = min((datetime.now() - listing_datetime).days, 90)
        sale_datetime = listing_datetime + timedelta(days=random.randint(0, days_variant))
        date_of_sale = listing_datetime.strftime('%Y-%m-%d')

        # decide sale price base on listing price with probability
        if random.random() < 0.6:   # sale price is the same as listing price
            sale_price = listing.listing_price
        else:   # sale price is different from listing price
            price_variant = int(listing.listing_price/1000/4)   # 25% of listing price in thousand dollar
            sale_price = listing.listing_price + 1000*random.randint(-price_variant,price_variant)

        # create sale object to insert
        sale = Sale(sale_price=sale_price,
                    date_of_sale=date_of_sale,
                    buyer=session.query(Buyer).get(random.randint(1,num_of_buyer)),
                    agent=agent,
                    office=office,
                    listing=listing)
        session.add(sale)
    session.commit()

    print ("Database seeded with random data")
