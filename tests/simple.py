from ..core import node
from ..core import csma

numOfNodes = 10
nodes = []
for i in range(numOfNodes):
	n = node.node()
	nodes.append(n)

for n in nodes:
	n.runNode(10000)
