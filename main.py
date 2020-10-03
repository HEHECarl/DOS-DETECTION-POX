from Controller.switch_stats import *
from Controller.onos import *


def main():
    print("Controller Start")
    onos = Onos("http://127.0.0.1:8181/onos/v1/", "onos", "rocks")
    ids_list = onos.get_all_switch_id()

    switches = []
    for i in ids_list:
        s = SwitchStats(i)
        onos.get_switch_stats(s)
        switches.append(s)


if __name__ == "__main__":
    main()
