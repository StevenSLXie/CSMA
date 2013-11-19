from source import source
from action import action
from pacGenerator import pacGenerator
from event import event
import operator



numOfNodes = 10
nodes = []
for i in range(numOfNodes):  # initialize nodes
	argv = {}
	argv['ID'] = i
	argv['src'] = i
	argv['des'] = numOfNodes - 1
	n = source(argv)
	nodes.append(n)

eventList = []
for i in range(numOfNodes-1):  # the last node as the sink
	for t in pacGenerator(1000*20,100,2000):
		argv = {}
		argv['time'] = t
		argv['actType'] = 'sendMac'
		argv['src'] = i
		argv['des'] = numOfNodes - 1
		argv['pacSize'] = 60
		argv['pacData'] = i
		argv['pacType'] = 'data'
		argv['pacAckReq'] = True
		e = event(argv)
		eventList.append(e)

while True:
	if not eventList:
		break
	else:
		min_index, min_t = min(enumerate(e.time for e in eventList),key=operator.itemgetter(1))
		newList = action(eventList[min_index],nodes)
		eventList.pop(min_index)
		for n in newList:
			eventList.append(n)

for i in range(numOfNodes-1):
	nodes[i].printPacStat()
	
		
	


