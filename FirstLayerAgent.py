from osbrain import Agent
from osbrain import run_agent
from colorama import Fore


class FirstLayerAgent(Agent):

    def on_init(self):
        self.events_table = []

    def custom_log(self, message):
        self.log_info('Received topic: %s' % message[26])
        self.events_table.append(message)


def create_first_layer_agents(topics):
    created_agents = []
    i = 1
    for topic in topics:
        name = 'agent1'+str(i)
        agent = run_agent(name, base=FirstLayerAgent, attributes=dict(topic=topic))
        created_agents.append(agent)
        print(Fore.GREEN + "First layer agent named: " + name + " CREATED" + "  TOPIC: " + topic + Fore.RESET)
        i += 1
    return created_agents


def connect_agents(agents, agent_to_address):
    for agent in agents:
        address = agent_to_address.bind('PUB', alias='main')
        agent.connect(address, handler={agent.get_attr('topic'): FirstLayerAgent.custom_log})


def publish_events(agents):
    for agent in agents:
        for message in agent.get_attr('events_table'):
            topic = str(message[26])[:2] + '|' + str(message[52])
            agent.send('main', message, topic=topic)
