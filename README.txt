# DOS-DETECTION-POX

usage: python3 main.py

NOTE
The following library need to be installed with latest version before lunching the program
-sklearn(require python 3.6 or above)
-requests
-json

This program is able to collect data from all the switches in the network, and analysis with a KNN Model,
the knn model will identify weather a host is a DoS attacker or just normal user
Once a attacker is found, the program will install a blocking rule on all switches to mitigate the DoS attack.

User Guide:
1 - Start up ONOS "onos-buck run onos-local -- clean"
2 - Start up a mininet, structure can be any "sudo mn –-topo tree,3,2 --mac –-controller remote"
3 - Start the main program by "python3 main.py"
4 - xterm the hosts you want to run client/server program
5 - For the host you want to run server, cd into the Client&Server Folder "python3 server.py"
6 - For the host you want to run normal user, cd into the Client&Server Folder "python3 normal_client.py {target_server} {frequency in second}"
7 - For the host you want to run attacker, cd into the Client&Server Folder "python3 attacker_client.py {target_server}"
8 - Then the main program will keep monitoring the network, it will print out the DoS attacker has found
