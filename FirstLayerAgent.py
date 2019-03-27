from osbrain import Agent
from osbrain import run_agent
from colorama import Fore


class FirstLayerAgent(Agent):

    def on_init(self):
        self.events_table = []

    def custom_log(self, message):
        self.log_info('Received topic: %s' % message[26])
        self.events_table.append(message)


def create_first_layer_agents(start_topic=1, stop_topic=21):
    agents = []
    topics = ["%.2d" % i for i in range(start_topic, stop_topic)]
    i = 1
    for topic in topics:
        name = 'agent1'+str(i)
        agent = run_agent(name, base=FirstLayerAgent, attributes=dict(topic=topic))
        agents.append(agent)
        print(Fore.GREEN + "First layer agent named: " + name + " CREATED" + Fore.RESET)
        i = i + 1
    return agents


def connect_agents(agents, agent_to_adress):
    for agent in agents:
        agent.connect(agent_to_adress.addr('main'), handler={agent.get_attr('topic'): FirstLayerAgent.custom_log})





