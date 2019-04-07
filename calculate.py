from datetime import datetime

from schema import Agent, Office, Listing, Sale, Cycle, AgentCommission, AgentSummary, OfficeSummary


def get_cycle(session, date_string):
    year, month, _ = date_string.split('-')
    year, month = int(year), int(month)
    cycle = session.query(Cycle).filter(Cycle.year==year, Cycle.month==month).first()
    if cycle == None:
        cycle = Cycle(year=year,
                      month=month)
        session.add(cycle)
        session.commit()
    return cycle


def get_agent_commission(session, agent_id, cycle_id):
    agent_commission = session.query(AgentCommission).filter_by(agent_id=agent_id, cycle_id=cycle_id).first()
    if agent_commission == None:
        agent_commission = AgentCommission(commission_amount=0,
                                           agent_id=agent_id,
                                           cycle_id=agent_id)
        session.add(agent_commission)
        session.commit()
    return agent_commission


def get_agent_summary(session, agent_id, cycle_id):
    agent_summary = session.query(AgentSummary).filter_by(agent_id=agent_id, cycle_id=cycle_id).first()
    if agent_summary == None:
        agent_summary = AgentSummary(total_sale=0,
                                     agent_id=agent_id,
                                     cycle_id=cycle_id)
        session.add(agent_summary)
        session.commit()
    return agent_summary


def get_office_summary(session, office_id, cycle_id):
    office_summary = session.query(OfficeSummary).filter_by(office_id=office_id, cycle_id=cycle_id).first()
    if office_summary == None:
        office_summary = OfficeSummary(total_sale=0,
                                       office_id=office_id,
                                       cycle_id=cycle_id)
        session.add(office_summary)
        session.commit()
    return office_summary


def calculate(session, sale):
    cycle = get_cycle(session, sale.date_of_sale)
    # calculate and update agent commission
    agent_commission = get_agent_commission(session, sale.agent_id, cycle.id)
    if sale.sale_price < 100000:
        commission = sale.sale_price * 0.1
    elif sale.sale_price < 200000:
        commission = sale.sale_price * 0.075
    elif sale.sale_price < 500000:
        commission = sale.sale_price * 0.06
    elif sale.sale_price < 1000000:
        commission = sale.sale_price * 0.05
    else:
        commission = sale.sale_price * 0.04
    agent_commission.commission_amount += commission
    # update agent summary
    agent_summary = get_agent_summary(session, sale.agent_id, cycle.id)
    agent_summary.total_sale += sale.sale_price
    # update office summary
    office_summary = get_office_summary(session, sale.office_id, cycle.id)
    office_summary.total_sale += sale.sale_price
    session.commit()
