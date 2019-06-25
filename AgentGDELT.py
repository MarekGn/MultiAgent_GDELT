from osbrain import Agent
from colorama import Fore
import requests
import lxml.html as lh
import os.path
import urllib
import zipfile
import glob
from collections import Counter
import operator
from settings import SCHEMA, AGENT_DATA
import pandas as pd

class AgentGDELT(Agent):

    def on_init(self):
        print(Fore.RED + "AgentGDELT Created" + Fore.RESET)
        if not os.path.exists('GDELT_Data/'):
            os.makedirs('GDELT_Data/tmp')
        self.gdelt_base_url = 'http://data.gdeltproject.org/events/'
        self.filtered_country_events = []
        self.country_code_occuring = []
        self.most_common_countries = []
        self.local_path = 'GDELT_Data/'
        self.file_list = self.getListOfLinks()

        self.correlated_countries = self.get_attr('correlated_countries')
        self.all_combinations_count = sum(list(range(1, len(self.correlated_countries))))
        self.aggressive_cameo_df = [pd.DataFrame() for _ in range(self.all_combinations_count)]
        self.full_df = [pd.DataFrame() for _ in range(self.all_combinations_count)]

        self.download_files()
        self.extract_files()
        self.filter_files()
        self.calculate_most_common_countries()

    def getListOfLinks(self):
        # get the list of all the links on the gdelt file page
        page = requests.get(self.gdelt_base_url + 'index.html')
        doc = lh.fromstring(page.content)
        link_list = doc.xpath("//*/ul/li/a/@href")

        # separate out those links that begin with four digits
        file_list = [x for x in link_list if str.isdigit(x[0:4])]
        filtered_file_list = [x for x in file_list if float(self.get_attr('date1')) <= float(x[0:4]) <= float(self.get_attr('date2'))]

        return filtered_file_list

    def download_files(self):
        for compressed_file in self.file_list:
            # if we dont have the compressed file stored locally, go get it. Keep trying if necessary.
            while not os.path.isfile(self.local_path + compressed_file):
                print('downloading {}'.format(compressed_file))
                urllib.request.urlretrieve(url=self.gdelt_base_url + compressed_file,
                                           filename=self.local_path + compressed_file)

    def extract_files(self):
        for compressed_file in self.file_list:
            # extract the contents of the compressed file to a temporary directory
            print('extracting {}'.format(compressed_file))
            z = zipfile.ZipFile(file=self.local_path + compressed_file, mode='r')
            z.extractall(path=self.local_path + 'tmp/')

    def filter_files(self):
        dtypes = SCHEMA['events']['columns-dtypes']
        use_cols = SCHEMA['events']['useful_cols']
        column_names = dtypes.keys()
        index = 0

        for infile_name in glob.glob(self.local_path + 'tmp/*'):
            print('parsing ' + infile_name)
            df = pd.read_csv(f'{infile_name}', delimiter="\t",
                             header=None, names=column_names, dtype=None, usecols=use_cols)
            for i in range(len(self.correlated_countries)):
                for j in range(i + 1, len(self.correlated_countries)):
                    self.aggressive_cameo_df[index] = pd.concat([self.aggressive_cameo_df[index], df.loc[
                        (df['actor1countrycode'].isin([self.correlated_countries[i], self.correlated_countries[j]])) & (
                        df['actor2countrycode'].isin([self.correlated_countries[i], self.correlated_countries[j]])) &
                        (df['actor1countrycode'] != df['actor2countrycode']) &
                        (df['eventrootcode'].isin(SCHEMA['events']['aggressive-cameo-families']))]])
                    self.full_df[index] = pd.concat([self.full_df[index], df.loc[
                        (df['actor1countrycode'].isin([self.correlated_countries[i], self.correlated_countries[j]])) & (
                        df['actor2countrycode'].isin([self.correlated_countries[i], self.correlated_countries[j]])) &
                        (df['actor1countrycode'] != df['actor2countrycode']) &
                        (df['eventrootcode'].isin(SCHEMA['events']['cameo-families']))]])
                    index += 1
            index = 0

            with open(infile_name, mode='r', encoding='utf8') as infile:
                for line in infile:
                    if len(line.split('\t')) >= 51:
                        # extract lines with our interest country code
                        if self.get_attr('country_code') == operator.itemgetter(17)(line.split('\t'))\
                                and operator.itemgetter(7)(line.split('\t')) != '' \
                                and operator.itemgetter(7)(line.split('\t')) != self.get_attr('country_code')\
                                and operator.itemgetter(28)(line.split('\t')) in self.get_attr('root_codes'):
                            self.filtered_country_events.append(line)
                            self.country_code_occuring.append(operator.itemgetter(7)(line.split('\t')))

                        elif self.get_attr('country_code') == operator.itemgetter(7)(line.split('\t'))\
                                and operator.itemgetter(17)(line.split('\t')) != ''\
                                and operator.itemgetter(17)(line.split('\t')) != self.get_attr('country_code')\
                                and operator.itemgetter(28)(line.split('\t')) in self.get_attr('root_codes'):
                            self.filtered_country_events.append(line)
                            self.country_code_occuring.append(operator.itemgetter(17)(line.split('\t')))
            # delete the temporary file
            os.remove(infile_name)

        for i in range(len(self.aggressive_cameo_df)):
            self.aggressive_cameo_df[i]['custom_coeff'] = self.aggressive_cameo_df[i]['numarticles'] * \
                                                     self.aggressive_cameo_df[i]['avgtone'] * self.aggressive_cameo_df[i][
                                                         'numsources'] * self.aggressive_cameo_df[i][
                                                         'goldsteinscale']
            self.full_df[i]['custom_coeff'] = self.full_df[i]['numarticles'] * self.full_df[i]['avgtone'] * self.full_df[i][
                'numsources'] * self.full_df[i]['goldsteinscale']

    def calculate_most_common_countries(self):
        occurs = Counter(self.country_code_occuring)
        occurs = occurs.most_common(self.get_attr('countries_amount'))
        self.most_common_countries = occurs

    def publish_gdelt(self):
        self.publish_stats_data_from_gdelt()
        for message in self.filtered_country_events:
            if operator.itemgetter(7)(message.split('\t')) == self.get_attr('country_code'):
                topic = operator.itemgetter(17)(message.split('\t'))
                self.send(AGENT_DATA['main_agent'], message, topic=topic)
            else:
                topic = operator.itemgetter(7)(message.split('\t'))
                self.send(AGENT_DATA['main_agent'], message, topic=topic)

    def publish_stats_data_from_gdelt(self):
        topic = AGENT_DATA['stats_agents_id'] + AGENT_DATA['full_data'] + ' ' + ' '.join(self.correlated_countries)
        self.send(AGENT_DATA['main_agent'], self.full_df, topic=topic)
        topic = AGENT_DATA['stats_agents_id'] + AGENT_DATA['aggressive_data']+' ' + ' '.join(self.correlated_countries)
        self.send(AGENT_DATA['main_agent'], self.aggressive_cameo_df, topic=topic)

    def get_len_comm_countries(self):
        return len(self.most_common_countries)