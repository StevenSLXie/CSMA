from source import source
from action import action
from pacGenerator import pacGenerator
from event import event
import operator
from initPacket import initPacket


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
	for t in pacGenerator(100*20,1,2000):
		e = initPacket(t,i,numOfNodes)
		eventList.append(e)

min_t  = 0
while True:
	if not eventList:
		break
	elif min_t > 5000000:
		break
	else:
		min_index, min_t = min(enumerate(e.time for e in eventList),key=operator.itemgetter(1))
		newList = action(eventList[min_index],nodes,2000)
		eventList.pop(min_index)
		for n in newList:
			eventList.append(n)

for i in range(numOfNodes-1):
#	nodes[i].printPacStat()
#	nodes[i].printDelayStat()
#	nodes[i].printEnergyStat()
	nodes[i].printChannelIndicators()
	
		
	


