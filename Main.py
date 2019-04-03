from osbrain import run_agent
from osbrain import run_nameserver
from AgentGDELT import AgentGDELT
import FirstLayerAgent
import SecondLayerAgents

if __name__ == '__main__':


        #TOPICS#
    # zagrożenie                13
    # protest                   14
    # pokazanie siły            15
    # ochłodzenie stosunków     16
    # wymuszenie                17
    # atak                      18

    # Inputs config
    topics = ['13', '14', '15', '16', '17', '18']
    regions = ['POL', 'GER', 'UA', 'VE']
    start_date = "2019 03 08"
    stop_date = "2019 03 14"
    events_limit = None

    # System deployment
    ns = run_nameserver()
    gd_agent = run_agent('GDELT', base=AgentGDELT)
    first_layer_agents = FirstLayerAgent.create_first_layer_agents(topics)
    second_layer_agents = SecondLayerAgents.create_second_layer_agents(regions, first_layer_agents)

    # System configuration
    FirstLayerAgent.connect_agents(first_layer_agents, gd_agent)
    SecondLayerAgents.connect_agents(second_layer_agents, first_layer_agents)

    # Send messages
    gd_agent.publish_gdelt(date1=start_date, date2=stop_date, table="events", output="pandas", limit=events_limit)
    FirstLayerAgent.publish_events(first_layer_agents)

    # Server shutdown
    ns.shutdown()
