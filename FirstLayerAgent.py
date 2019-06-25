from osbrain import Agent
from osbrain import run_agent
from colorama import Fore
import operator
from settings import AGENT_DATA, STATS_DATA
import pandas as pd

class FirstLayerAgent(Agent):

    def on_init(self):
        self.filtered_country_events = []
        self.stats_data = pd.DataFrame()

    def custom_log(self, message):
        self.filtered_country_events.append(message)

    def stats_log(self, message):
        self.stats_data = message

    def is_stats_agent(self):
        return self.get_attr('topic')[0] == AGENT_DATA['stats_agents_id']


def create_first_layer_agents(gd_agent):
    topics = [x[0] for x in gd_agent.get_attr('most_common_countries')]
    stats_topic = [AGENT_DATA['stats_agents_id'] + AGENT_DATA['full_data']
                   + ' ' + ' '.join(gd_agent.get_attr('correlated_countries')),
                   AGENT_DATA['stats_agents_id'] + AGENT_DATA['aggressive_data']
                   + ' ' + ' '.join(gd_agent.get_attr('correlated_countries'))]
    topics.extend(stats_topic)
    created_agents = []
    agent_number = 1

    for agent_topic in topics:
        name = 'agent1'+str(agent_number)
        agent = run_agent(name, base=FirstLayerAgent, attributes=dict(topic=agent_topic))
        created_agents.append(agent)
        print(Fore.GREEN + "First layer agent named: " + name + " CREATED" + "  TOPIC: " + agent_topic + Fore.RESET)
        agent_number += 1
    return created_agents


def connect_agents(agents, agent_to_address):
    address = agent_to_address.bind('PUB', alias='main')
    for agent in agents:
        if agent.is_stats_agent():
            agent.connect(address, handler={agent.get_attr('topic'): FirstLayerAgent.stats_log})
        else:
            agent.connect(address, handler={agent.get_attr('topic'): FirstLayerAgent.custom_log})


def publish_events(agents, countrycode):
    for agent in agents:
        if agent.is_stats_agent():
            for scale in STATS_DATA['scales']:
                for kind_of_stat in STATS_DATA['kind_of_stat']:
                    topic = agent.get_attr('topic') + '|' + scale + '|' + kind_of_stat
                    stats_data = agent.get_attr('stats_data')
                    grouped_data = []
                    for i in stats_data:
                        grouped_data.append(i.groupby(['year']).mean())

                    agent.send('main', grouped_data, topic=topic)
        else:
            for message in agent.get_attr('filtered_country_events'):
                if operator.itemgetter(7)(message.split('\t')) == countrycode:
                    topic = operator.itemgetter(17)(message.split('\t')) + '|' + operator.itemgetter(28)(message.split('\t'))
                    agent.send('main', message, topic=topic)
                else:
                    topic = operator.itemgetter(7)(message.split('\t')) + '|' + operator.itemgetter(28)(message.split('\t'))
                    agent.send('main', message, topic=topic)