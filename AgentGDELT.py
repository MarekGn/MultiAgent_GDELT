import gdelt
from osbrain import Agent
from colorama import Fore


class AgentGDELT(Agent):

    def on_init(self):
        self.bind('PUB', alias='main')
        self.gd1 = gdelt.gdelt(version=1)
        print(Fore.RED + "AgentGDELT Created" + Fore.RESET)

        if(self.get_attr('date2') is None):
            print(Fore.RED + "*DOWNLOADING GDELT RESULTS IN PROGRESS*" + Fore.RESET)
            self.results = self.gd1.Search([self.get_attr('date1')],
                                           table=self.get_attr('table'), output=self.get_attr('output'))
            self.results = self.results.head(self.get_attr('limit'))
            print(Fore.RED + "GDELT RESULTS DOWNLOADED WITH " + str(len(self.results)) + " RECORDS" + Fore.RESET)
        else:
            print(Fore.RED + "*DOWNLOADING GDELT RESULTS IN PROGRESS*" + Fore.RESET)
            self.results = self.gd1.Search([self.get_attr('date1'), self.get_attr('date2')],
                                           table=self.get_attr('table'), output=self.get_attr('output'))
            self.results = self.results.head(self.get_attr('limit'))
            print(Fore.RED + "GDELT RESULTS DOWNLOADED WITH " + str(len(self.results)) + " RECORDS" + Fore.RESET)

    def publish_gdelt(self):
        for message in self.get_attr('results').values:
            topic = str(message[26])[:2]
            self.send('main', message, topic=topic)
