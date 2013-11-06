from node import node
from csma import csma

numOfNodes = 20
nodes = []

#net = csma()
#net.seqSorted(seq)

for i in range(numOfNodes):
	n = node(i)
	nodes.append(n)

for n in nodes:
	n.packetGenerator()

time = 0
while time < 10000:
	time = time + 1
	nodeCol = 0
	for n in nodes:
		if time in n.getLocalChannel():
			nodeCol = nodeCol + 1
	for n in nodes:
		if time in n.getLocalChannel():
			if nodeCol > 1: 
				n.send(time,1)
			else:
				n.send(time,0)

for n in nodes:
	n.showResult()

#print csma.channelOccupy
