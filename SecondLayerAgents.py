from osbrain import Agent
from osbrain import run_agent
from colorama import Fore
import matplotlib.pyplot as plt
from textwrap import wrap
import os


class SecondLayerAgent(Agent):

    def on_init(self):
        self.events_table = []

    def custom_log(self, message):
        self.events_table.append(message)


def create_second_layer_agents(cameo_codes, first_layer_agents):
    created_agents = []
    i = 1
    for code in cameo_codes:
        for first_layer_agent in first_layer_agents:
            name = 'agent2'+str(i)
            topic = first_layer_agent.get_attr('topic') + '|' + code
            agent = run_agent(name, base=SecondLayerAgent, attributes=dict(topic=topic))
            created_agents.append(agent)
            print(Fore.BLUE + "Second layer agent named: " + name + " CREATED" + "  TOPIC: " + topic + Fore.RESET)
            i += 1
    return created_agents


def connect_agents(agents, agents_to_address):
    addresses = []
    for agent_to_address in agents_to_address:
        addresses.append(agent_to_address.bind('PUB', alias='main'))
    for agent in agents:
        for address in addresses:
            agent.connect(address, handler={agent.get_attr('topic'): SecondLayerAgent.custom_log})


def plot_countries_interaction(agents, root_codes, country_code, start_date, stop_date):
    if not os.path.exists('Figures/'):
        os.makedirs('Figures/')
    for plot_code in root_codes:
        fig, ax = plt.subplots()
        plt.rcdefaults()
        countries = []
        number_events = []
        for agent in agents:
            if agent.get_attr('topic')[-2:] == plot_code:
                country_name = agent.get_attr('topic').split('|')[0]
                countries.append(country_name)
                number_events.append(len(agent.get_attr('events_table')))
        ax.bar(tuple(countries), tuple(number_events), align='center', color='blue')
        ax.set_xlabel('Countries')
        ax.set_ylabel('Number of events')
        ax.set_title('\n'.join(wrap('COUNTRIES SELECTED BY {} \n Countries with the biggest interaction having a {} '
                                    'CAMEO code  with {} from {} to {}'
                     .format(root_codes, plot_code, country_code, stop_date, start_date))))

        #save plots without overwriting
        i = 0
        filename = country_code + plot_code + 'country interaction'
        while os.path.exists('{}{:d}.png'.format(filename, i)):
            i += 1
        plt.savefig('Figures/{}{:d}.png'.format(filename, i))

