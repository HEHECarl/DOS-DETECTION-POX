from Controller.switch_stats import *
from Controller.onos import *
from KMean.kmean import *
import time


def main():
    print("Controller Start")
    onos = Onos("http://127.0.0.1:8181/onos/v1/", "onos", "rocks")
    ids_list = onos.get_all_switch_id()

    switches = []
    for i in ids_list:
        s = SwitchStats(i)
        onos.get_switch_stats(s)
        switches.append(s)

    while True:
        for s in switches:
            onos.get_switch_stats(s)
            for f in s.stats['flows']:
                if f['appId'] == 'org.onosproject.fwd':
                    count = f['packets']
                    src = f['selector']['criteria'][2]['mac']
                    dst = f['selector']['criteria'][1]['mac']
                    print("{} {} {}".format(src, dst, count))
    time.sleep(1)


if __name__ == "__main__":
    main()
