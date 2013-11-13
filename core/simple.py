from node import node
from csma import csma

numOfNodes = 10
nodes = []
simTime = 10000

#net = csma()
#net.seqSorted(seq)

for i in range(numOfNodes):
	n = node(i)
	nodes.append(n)

# sender nodes
for i in range(len(nodes)-1):
	nodes[i].senderPacketGenerator()
# sink node
nodes[len(nodes)-1].sinkPacketGenerator(simTime)

time = 0
while time < simTime-1:
	time = time + 1
	for n in nodes:
		n.updateCurTime(time)

	for i in range(len(nodes)-1):
		if time in nodes[i].getLocalChannel():
			action = nodes[i].getCurrentAction(time)
#			print action
			if action == 1:
				nodes[i].channelSensing(time)
			elif action == 2:
				nodes[i].sendingData(time)
			elif action == 3:
				nodes[i].waitingACK(time)
			elif action == 0:
				nodes[i].receiveData(time,3)
#	print time
	if time in nodes[-1].getLocalChannel():
		action = nodes[-1].getCurrentAction(time)
		if action == 0:
			nodes[-1].receiveData(time,3)

for n in nodes:
	n.showResult()
#print nodes[len(nodes)-1].getLocalChannel()

#print csma.channelOccupy
#	print n.curTime

#print csma.channelOccupy

