import requests
import json
from Controller.switch_stats import *


class Onos:
    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password

    def get_all_switch_id(self):
        request = self.address + "devices"
        res = requests.get(url=request, auth=(self.username, self.password)).json()
        ids_list = []
        for i in res['devices']:
            ids_list.append(i['id'])

        return ids_list

    def get_switch_stats(self, switch_stats):
        request = self.address + "flows/" + switch_stats.id
        response = requests.get(url=request, auth=(self.username, self.password)).json()
        switch_stats.stats = response

    def deny_host(self, src, dst):
        f = open("deny.jason")
        data = json.load(f)
        data["selector"]["criteria"][0]["mac"] = src
        data["selector"]["criteria"][1]["mac"] = dst
        ids_list = self.get_all_switch_id()
        for id in ids_list:
            request = self.address + "flows/" + id
            requests.post(url=request, json=data, auth=(self.username, self.password))
        print("Installed rules on switches to block connection from {} to {}".format(src, dst))
