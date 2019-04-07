from sqlalchemy import desc
import inflect

from schema import Cycle, AgentSummary, AgentCommission, OfficeSummary

p = inflect.engine()


def print_report(session, year, month):
    print ("\n### Report For Year {:d} Month {:d} ###\n".format(year, month))
    cycle = session.query(Cycle).filter(Cycle.year==year, Cycle.month==month).first()
    if cycle == None:
        print ("No data for the cycle requested")
        return

    # agent sale ranking for top 5
    agent_summarys = session.query(AgentSummary).filter_by(cycle_id=cycle.id).order_by(desc(AgentSummary.total_sale)).limit(5).all()
    for key, summary in enumerate(agent_summarys):
        print ("The {:s} agent is {:s} {:s} with total sale of {:d}".format(p.ordinal(key+1),
                                                                            summary.agent.first_name,
                                                                            summary.agent.last_name,
                                                                            summary.total_sale))
        print ("Phone number: {:s} Email address: {:s}".format(summary.agent.phone_number,
                                                                                  summary.agent.email_address))

        # get commission amount for agent
        commission = session.query(AgentCommission).filter_by(cycle_id=cycle.id, agent_id=summary.agent.id).first()
        print ("Commission to be paied: {:d}".format(commission.commission_amount))


    print ("\n------------\n")

    # office sale ranking for top 5
    office_summarys = session.query(OfficeSummary).filter_by(cycle_id=cycle.id).order_by(desc(OfficeSummary.total_sale)).limit(5).all()
    for key, summary in enumerate(office_summarys):
        print ("The {:s} office is {:s} with total sale of {:d}".format(p.ordinal(key+1),
                                                                        summary.office.name,
                                                                        summary.total_sale))
        print ("Office location: {:s}".format(summary.office.address))

    print ("\n### End of Report\n")
