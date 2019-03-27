from osbrain import run_agent
from osbrain import run_nameserver
from AgentGDELT import AgentGDELT
import FirstLayerAgent

if __name__ == '__main__':

    # System deployment
    ns = run_nameserver()
    gd_agent = run_agent('GDELT', base=AgentGDELT)
    first_layer_agents = FirstLayerAgent.create_first_layer_agents(1, 21)

    # System configuration
    FirstLayerAgent.connect_agents(first_layer_agents, gd_agent)

    # Send messages
    gd_agent.publish_gdelt(date1="2019 03 13", date2="2019 03 14", table="events", output="pandas", limit=5000)

    ns.shutdown()
