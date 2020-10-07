from Controller.onos import *
from Controller.switch_stats import *
from KNN.knn import *
from copy import deepcopy
import time

ONOS_ADDRESS = "http://127.0.0.1:8181/onos/v1/"
ONOS_USERNAME = "onos"
ONOS_PASSWORD = "rocks"


class Controller:
    def __init__(self, mode, attackers):
        self.onos = Onos(ONOS_ADDRESS, ONOS_USERNAME, ONOS_PASSWORD)
        self.ids_list = self.onos.get_all_switch_id()
        self.switches = []
        for i in self.ids_list:
            s = SwitchStats(i)
            self.switches.append(s)
        self.count_dict = {}
        self.current_count_dict = {}
        self.mode = mode
        if self.mode == "learn":
            self.file = open("data.txt", "a")
        else:
            self.model = KNN()
            self.model.import_Data("data.txt")
            self.model.fit()
        self.attackers = attackers

    def start(self):
        print("Controller Start")
        while True:
            for s in self.switches:
                self.onos.get_switch_stats(s)
                for f in s.stats['flows']:
                    if f['appId'] == 'org.onosproject.fwd':
                        count = f['packets']
                        src = f['selector']['criteria'][2]['mac']
                        dst = f['selector']['criteria'][1]['mac']
                        self.record_count(src, dst, count)
            c = self.get_difference()
            if self.mode == "learn":
                self.learn_model(c)
            else:
                self.check_attacker(c)
            time.sleep(5)

    def record_count(self, src, dst, count):
        if src in self.current_count_dict:
            if dst in self.current_count_dict[src]:
                if count > self.current_count_dict[src][dst]:
                    self.current_count_dict[src][dst] = count
            else:
                self.current_count_dict[src][dst] = count
        else:
            self.current_count_dict[src] = {}
            self.current_count_dict[src][dst] = count

    def check_attacker(self, difference_count_dict):
        for key_src, value in difference_count_dict.items():
            for key_dst, src_dst_count in value.items():
                if int(key_dst.split(':')[5]) > int(key_src.split(':')[5]):
                    try:
                        dst_src_count = difference_count_dict[key_dst][key_src]
                        is_attacker = False
                        if src_dst_count >= dst_src_count:
                            is_attacker = self.model.predict([[src_dst_count, dst_src_count]]) == [1]
                        else:
                            is_attacker = self.model.predict([[dst_src_count, src_dst_count]]) == [1]

                        if is_attacker:
                            if src_dst_count >= dst_src_count:
                                print("Attack Found at {} targeting {}".format(key_src, key_dst))
                            else:
                                print("Attack Found at {} targeting {}".format(key_dst, key_src))
                    except:
                        print("Error\n")

    def learn_model(self, difference_count_dict):
        for key_src, value in difference_count_dict.items():
            for key_dst, src_dst_count in value.items():
                if int(key_dst.split(':')[5]) > int(key_src.split(':')[5]):
                    try:
                        dst_src_count = difference_count_dict[key_dst][key_src]
                        if int(key_src.split(':')[5]) in self.attackers or int(key_dst.split(':')[5]) in self.attackers:
                            if src_dst_count >= dst_src_count:
                                self.file.write("{} {} {}\n".format(src_dst_count, dst_src_count, 1))
                                print("{} {} {}\n".format(src_dst_count, dst_src_count, 1))
                            else:
                                self.file.write("{} {} {}\n".format(dst_src_count, src_dst_count, 1))
                                print("{} {} {}\n".format(dst_src_count, src_dst_count, 1))
                        else:
                            if src_dst_count >= dst_src_count:
                                self.file.write("{} {} {}\n".format(src_dst_count, dst_src_count, 0))
                                print("{} {} {}\n".format(src_dst_count, dst_src_count, 0))
                            else:
                                self.file.write("{} {} {}\n".format(dst_src_count, src_dst_count, 0))
                                print("{} {} {}\n".format(dst_src_count, src_dst_count, 0))
                    except:
                        print("Error\n")

    def get_difference(self):
        differenct_dict = {}
        for key_src, value in self.current_count_dict.items():
            if key_src in self.count_dict:
                differenct_dict[key_src] = {}
                try:
                    for key_dst, src_dst_count in value.items():
                        if key_dst in self.count_dict:
                            differenct_dict[key_src][key_dst] = src_dst_count - self.count_dict[key_src][key_dst]
                        else:
                            differenct_dict[key_src][key_dst] = src_dst_count
                except:
                    print("Error")
            else:
                differenct_dict[key_src] = value
        self.count_dict = deepcopy(self.current_count_dict)
        self.current_count_dict = {}
        return differenct_dict
