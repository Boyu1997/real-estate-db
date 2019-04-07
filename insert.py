from schema import Agent, Office, Buyer, House, Listing, Sale


def new_agent(session, firest_name, last_name, phone_number, email_address):
    agent = Agent(firest_name=firest_name,
                  last_name=last_name,
                  phone_number=phone_number,
                  email_address=email_address)
    session.add(agent)
    session.commit()
    print ("New aget created with first name {:s}".format(firest_name))


def new_office_with_agents(session, name, address, agent_ids):
    agents = [session.query(Agent).get(id) for id in agent_ids]
    office = Office(name=name,
                    address=address,
                    agents=agents)
    session.add(office)
    session.commit()
    print ("New office created with {:d} agents".format(len(agent_ids)))


def new_listing(session, num_of_bedroom, num_of_bathroom, address, zipcode,
                listing_price, date_of_listing, agent_id, office_id):
    # create house
    house = House(num_of_bedroom=num_of_bedroom,
                  num_of_bathroom=num_of_bathroom,
                  address=address,
                  zipcode=zipcode)
    session.add(house)

    # create listing
    listing = Listing(listing_price=listing_price,
                      date_of_listing=date_of_listing,
                      status='available',
                      agent=session.query(Agent).get(agent_id),
                      office=session.query(Office).get(office_id),
                      house=house)
    session.add(listing)

    session.commit()
    print ("New listing created with price {:d}".format(listing_price))


def new_sale(session, firest_name, last_name, phone_number, email_address, sale_price,
             date_of_sale, agent_id, office_id, listing_id):
    # create buyer
    buyer = Buyer(firest_name=firest_name,
                  last_name=last_name,
                  phone_number=phone_number,
                  email_address=email_address)
    session.add(buyer)

    # update listing status to sold
    listing = session.query(Listing).get(listing_id)
    listing.status = 'sold'

    # create sale
    sale = Sale(sale_price=sale_price,
                date_of_sale=date_of_sale,
                buyer=buyer,
                agent=session.query(Agent).get(agent_id),
                office=session.query(Office).get(office_id),
                listing=listing)
    session.add(sale)

    session.commit()
    print ("New sale created with price {:d}".format(sale_price))
