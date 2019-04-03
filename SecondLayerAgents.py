from osbrain import Agent
from osbrain import run_agent
from colorama import Fore


class SecondLayerAgent(Agent):

    def on_init(self):
        self.events_table = []

    def custom_log(self, message):
        self.log_info('Received topic: %s' % message[52])
        self.events_table.append(message)


def create_second_layer_agents(regions, first_layer_agents):
    created_agents = []
    i = 1
    for region in regions:
        for first_layer_agent in first_layer_agents:
            name = 'agent2'+str(i)
            topic = first_layer_agent.get_attr('topic') + '|' + region
            agent = run_agent(name, base=SecondLayerAgent, attributes=dict(topic=topic))
            created_agents.append(agent)
            print(Fore.BLUE + "Second layer agent named: " + name + " CREATED" + "  TOPIC: " + topic + Fore.RESET)
            i += 1
    return created_agents


def connect_agents(agents, agents_to_address):
    for agent in agents:
        for agent_to_address in agents_to_address:
            address = agent_to_address.bind('PUB', alias='main')
            agent.connect(address, handler={agent.get_attr('topic'): SecondLayerAgent.custom_log})