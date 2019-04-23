from osbrain import run_agent
from osbrain import run_nameserver
from AgentGDELT import AgentGDELT
import FirstLayerAgent
import SecondLayerAgents
import sys

if __name__ == '__main__':
    # TOPICS#
    # dostarczenie pomocy       07
    # zagrożenie                13
    # protest                   14
    # pokazanie siły            15
    # ochłodzenie stosunków     16
    # wymuszenie                17
    # atak                      18
    # walka                     19
    # przemoc masowa            20

    ####################################################################################################################
    # Inputs config
    start_date, stop_date = '2006', '1979'
    most_common_countries = 20
    country_code = 'PL'
    root_codes = ['18', '19', '20']

    # System deployment
    ns = run_nameserver()
    gd_agent = run_agent('GDELT', base=AgentGDELT, attributes=dict(date1=start_date, date2=stop_date,
                                                                   country_code=country_code, root_codes=root_codes,
                                                                   countries_amount=most_common_countries))
    if gd_agent.get_len_comm_countries() == 0:
        print("There are no countries with given interaction")
        sys.exit()

    first_layer_agents = FirstLayerAgent.create_first_layer_agents(gd_agent)
    second_layer_agents = SecondLayerAgents.create_second_layer_agents(root_codes, first_layer_agents)

    # System configuration
    FirstLayerAgent.connect_agents(first_layer_agents, gd_agent)
    SecondLayerAgents.connect_agents(second_layer_agents, first_layer_agents)

    # Send messages
    gd_agent.publish_gdelt()
    FirstLayerAgent.publish_events(first_layer_agents, country_code)

    # Plot informations
    SecondLayerAgents.plot_countries_interaction(second_layer_agents, root_codes, country_code, start_date, stop_date)

    # Server shutdown
    ns.shutdown()

