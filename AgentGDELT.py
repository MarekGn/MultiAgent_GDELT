import gdelt
from osbrain import Agent
from colorama import Fore
import time


class AgentGDELT(Agent):

    def on_init(self):
        self.bind('PUB', alias='main')
        self.gd1 = gdelt.gdelt(version=1)
        print(Fore.RED + "AgentGDELT Created" + Fore.RESET)

    def publish_gdelt(self, date1, date2=None, table='events', output='pandas', limit=None):
        if(date2 is None):
            results = self.gd1.Search([date1], table=table, output=output)
            results = results.head(limit)
        else:
            results = self.gd1.Search([date1, date2], table=table, output=output)
            results = results.head(limit)

        for each in results.values:
            topic = str(each[26])[:2]
            message = each
            self.send('main', message, topic=topic)