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
        for compressed_file in self.file_list:
            for infile_name in glob.glob(self.local_path + 'tmp/*'):
                print('parsing ' + infile_name)
                # open the infile
                with open(infile_name, mode='r', encoding='utf8') as infile:
                    for line in infile:
                        if (len(line.split('\t')) >= 51):
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

    def calculate_most_common_countries(self):
        occurs = Counter(self.country_code_occuring)
        occurs = occurs.most_common(self.get_attr('countries_amount'))
        self.most_common_countries = occurs


    def publish_gdelt(self):
        for message in self.filtered_country_events:
            if operator.itemgetter(7)(message.split('\t')) == self.get_attr('country_code'):
                topic = operator.itemgetter(17)(message.split('\t'))
                self.send('main', message, topic=topic)
            else:
                topic = operator.itemgetter(7)(message.split('\t'))
                self.send('main', message, topic=topic)

    def get_len_comm_countries(self):
        return len(self.most_common_countries)