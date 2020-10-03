import requests
from Controller.switch_stats import *


class Onos:
    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password

    def get_all_switch_id(self):
        request = self.address + "devices"
        res = requests.get(url=request, auth=(self.username, self.password)).json()

        ids_list = (i['devices'] for i in res)

        return ids_list

    def get_switch_stats(self, switch_stats):
        request = self.address + "flows/" + switch_stats.id
        response = requests.get(url=request, auth=(self.username, self.password)).json()
        switch_stats.stats = response