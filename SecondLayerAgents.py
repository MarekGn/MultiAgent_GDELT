from osbrain import Agent
from osbrain import run_agent
from colorama import Fore
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
from textwrap import wrap
import os
from settings import AGENT_DATA, STATS_DATA, PLOT_DATA
import numpy as np
from collections import Counter, defaultdict


class SecondLayerAgent(Agent):

    def on_init(self):
        self.events_table = []

    def custom_log(self, message):
        self.events_table.append(message)

    def stats_log(self, message):
        self.stats_data = message

    def is_stats_agent(self):
        return self.get_attr('topic')[0] == AGENT_DATA['stats_agents_id']


def create_second_layer_agents(cameo_codes, first_layer_agents):
    created_agents = []
    i = 1
    stats_agents = [a for a in first_layer_agents if a.get_attr('topic')[0] == AGENT_DATA['stats_agents_id']]
    cameo_agents = [a for a in first_layer_agents if a.get_attr('topic')[0] != AGENT_DATA['stats_agents_id']]

    for code in cameo_codes:
        for agent in cameo_agents:
            topic = agent.get_attr('topic') + '|' + code
            create_agent(i, topic, created_agents)
            i += 1

    for scale in STATS_DATA['scales']:
        for kind_of_stat in STATS_DATA['kind_of_stat']:
            for agent in stats_agents:
                topic = agent.get_attr('topic') + '|' + scale + '|' + kind_of_stat
                create_agent(i, topic, created_agents)
                i += 1
    return created_agents


def create_agent(index, topic, created_agents):
    name = 'agent2' + str(index)
    agent = run_agent(name, base=SecondLayerAgent, attributes=dict(topic=topic))
    created_agents.append(agent)
    print(Fore.BLUE + "Second layer agent named: " + name + " CREATED" + "  TOPIC: " + topic + Fore.RESET)


def connect_agents(agents, agents_to_address):
    addresses = []
    for agent_to_address in agents_to_address:
        addresses.append(agent_to_address.bind('PUB', alias='main'))
    for agent in agents:
        if agent.is_stats_agent():
            for address in addresses:
                agent.connect(address, handler={agent.get_attr('topic'): SecondLayerAgent.stats_log()})
        else:
            for address in addresses:
                agent.connect(address, handler={agent.get_attr('topic'): SecondLayerAgent.custom_log()})


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
        c = zip(number_events, countries)
        c = sorted(c, reverse=True)
        number_events, countries = zip(*c)
        ax.bar(tuple(countries), tuple(number_events), align='center', color='blue')
        ax.set_xlabel('Countries')
        ax.set_ylabel('Number of events')
        ax.set_title('\n'.join(wrap('COUNTRIES SELECTED BY {} \n Countries with the biggest interaction having a {} '
                                    'CAMEO code  with {} from {} to {}'
                     .format(root_codes, plot_code, country_code, stop_date, start_date))))

        #save plots without overwriting
        i = 0
        filename = country_code + plot_code + 'country interaction'
        while os.path.exists('Figures/{}{:d}.png'.format(filename, i)):
            i += 1
        plt.savefig('Figures/{}{:d}.png'.format(filename, i))


def calculate_correlations_and_find_allies(agents, all_combinations_count, countries):
    if not os.path.exists('Results/'):
        os.makedirs('Results/')

    scales = STATS_DATA['scales']
    labels = [' ']
    for i in range(len(countries)):
        for j in range(i + 1, len(countries)):
            labels.append(countries[i] + '-' + countries[j])

    for agent in agents:
        topic = agent.get_attr('topic')
        kind_of_data = ''
        if AGENT_DATA['full_data'] in topic:
            kind_of_data = PLOT_DATA['full_data']
        elif AGENT_DATA['aggressive_data'] in topic:
            kind_of_data = PLOT_DATA['aggressive_data']

        stats_data = agent.get_attr('stats_data')
        cameos_corrs = {k: np.full((all_combinations_count, all_combinations_count), 0.) for k in scales}
        for i in range(0, all_combinations_count):
            for j in range(0, all_combinations_count):
                for scale in scales:
                    cameos_corrs[scale][i][j] = stats_data[i][scale].corr(
                        stats_data[j][scale])

        for scale in scales:
            fig = plt.figure(figsize=(12, 10))
            fig.suptitle(f'{kind_of_data} behaviours correlation beetween countries by scale: {scale}', fontsize=24)
            ax = fig.add_subplot(111)
            cax = ax.matshow(cameos_corrs[scale])
            fig.colorbar(cax)

            ax.set_xticklabels(labels, rotation=-55, fontsize=9)
            ax.set_yticklabels(labels, fontsize=9)
            ax.xaxis.set_ticks_position('bottom')
            ax.xaxis.set_major_locator(MultipleLocator(1))
            ax.yaxis.set_major_locator(MultipleLocator(1))
            i = 0
            filename = kind_of_data + 'correlation' + ' '.join(countries)
            while os.path.exists('Figures/{}{:d}.png'.format(filename, i)):
                i += 1
            plt.savefig('Figures/{}{:d}.png'.format(filename, i))

        cameo_counts = []
        for i in stats_data:
            cameo_counts.append(i.groupby(['eventrootcode']).size().reset_index(name='counts'))
        not_familiar = []
        familiar = []
        ratios = []
        for i in range(all_combinations_count):
            not_familiar.append(
                cameo_counts[i][cameo_counts[i]['eventrootcode'].astype(int) >= 13].sum().counts)
            familiar.append(cameo_counts[i][cameo_counts[i]['eventrootcode'].astype(int) < 13].sum().counts)
            ratios.append(not_familiar[i] / familiar[i])

        pair_of_countries = []
        for i in range(len(countries)):
            for j in range(i + 1, len(countries)):
                pair_of_countries.append((countries[i], countries[j]))

        aggresive_countries = []
        non_aggresive_countries = []
        all_countries = []
        for i in range(len(ratios)):
            if ratios[i] > 0.3:
                aggresive_countries.append((i, pair_of_countries[i]))
            elif ratios[i] < 0.2:
                non_aggresive_countries.append((i, pair_of_countries[i]))
            all_countries.append((i, pair_of_countries[i]))

        agressive_corrs = []
        for pair in aggresive_countries:
            high_corr = np.where(cameos_corrs['custom_coeff'][pair[0]] > 0.6)
            related_countries = [i[0] for i in all_countries if any(n in i[1] for n in pair[1])]
            agressive_corrs.append(list(set(high_corr[0].tolist()).intersection(set(related_countries))))

        cnt = Counter(sum(agressive_corrs, []))
        feud_occurences = []
        for pair in cnt:
            feud_occurences.append((all_countries[pair][1], cnt[pair]))

        feuds_dict = defaultdict(list)
        for feud in feud_occurences:
            feuds_dict[feud[0][0]].append(feud[0][1])
            feuds_dict[feud[0][1]].append(feud[0][0])
        feuds = [[k] + v for k, v in feuds_dict.items()]

        alliances = []
        for m_feud in feuds:
            for feud in feuds:
                if m_feud[0] in feud:
                    continue
                common_enemies = list(set(feud).intersection(set(m_feud)))
                if len(common_enemies) > 0:
                    allies = [x[0] for x in alliances]
                    enemies = [x[1] for x in alliances]
                    for enemy in common_enemies:
                        if not ((feud[0], m_feud[0]) in allies and enemy in enemies):
                            alliances.append(((m_feud[0], feud[0]), enemy))

        with open(f"""Results/Feuds_{kind_of_data}_{' '.join(countries)}.txt""", 'w', encoding='utf-8') as file:
            file.write(feuds)
        with open(f"""Results/Allies_{kind_of_data}_{' '.join(countries)}.txt""", 'w', encoding='utf-8') as file:
            file.write(alliances)


def plot_trends(agents, countries):
    labels = []
    for i in range(len(countries)):
        for j in range(i + 1, len(countries)):
            labels.append(countries[i] + '-' + countries[j])
    for agent in agents:
        topic = agent.get_attr('topic')
        stats_data = agent.get_attr('stats_data')
        kind_of_data = ''
        if AGENT_DATA['full_data'] in topic:
            kind_of_data = PLOT_DATA['full_data']
        elif AGENT_DATA['aggressive_data'] in topic:
            kind_of_data = PLOT_DATA['aggressive_data']
        for i in range(len(labels)):
            ax = plt.gca()
            ax.xaxis.set_major_locator(MultipleLocator(2))
            plt.title(f'Trend line of {kind_of_data} behaviours between {labels[i]}')
            stats_data[i].plot(kind='line', y='custom_coeff', ax=ax)
            i = 0
            filename = kind_of_data + 'correlation' + ' '.join(countries)
            while os.path.exists('Figures/{}{:d}.png'.format(filename, i)):
                i += 1
            plt.savefig('Figures/{}{:d}.png'.format(filename, i))