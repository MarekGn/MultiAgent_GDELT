from osbrain import Agent
from osbrain import run_agent
from colorama import Fore
import operator


class FirstLayerAgent(Agent):

    def on_init(self):
        self.filtered_country_events = []

    def custom_log(self, message):
        self.filtered_country_events.append(message)


def create_first_layer_agents(gd_agent):
    topics = gd_agent.get_attr('most_common_countries')
    created_agents = []
    agent_number = 1

    for agent_topic in topics:
        name = 'agent1'+str(agent_number)
        agent = run_agent(name, base=FirstLayerAgent, attributes=dict(topic=agent_topic[0]))
        created_agents.append(agent)
        print(Fore.GREEN + "First layer agent named: " + name + " CREATED" + "  TOPIC: " + agent_topic[0] + Fore.RESET)
        agent_number += 1
    return created_agents


def connect_agents(agents, agent_to_address):
    address = agent_to_address.bind('PUB', alias='main')
    for agent in agents:
        agent.connect(address, handler={agent.get_attr('topic'): FirstLayerAgent.custom_log})


def publish_events(agents, countrycode):
    for agent in agents:
        for message in agent.get_attr('filtered_country_events'):
            if operator.itemgetter(7)(message.split('\t')) == countrycode:
                topic = operator.itemgetter(17)(message.split('\t')) + '|' + operator.itemgetter(28)(message.split('\t'))
                agent.send('main', message, topic=topic)
            else:
                topic = operator.itemgetter(7)(message.split('\t')) + '|' + operator.itemgetter(28)(message.split('\t'))
                agent.send('main', message, topic=topic)