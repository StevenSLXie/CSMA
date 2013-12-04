from source import source
from action import action
from pacGenerator import pacGenerator
from event import event
import operator
from initPacket import initPacket
import math
import random
import csv

def runSimulation(dataRate):
	numOfNodes = 20
	nodes = []
	for i in range(numOfNodes):  # initialize nodes
		argv = {}
		argv['ID'] = i
		argv['src'] = i
		argv['des'] = numOfNodes - 1
		n = source(argv)
		nodes.append(n)

	eventList = []
	for i in range(numOfNodes-1):
		nodes[i].setPacInterval(dataRate)

	for i in range(numOfNodes-1):  # the last node as the sink
		for t in pacGenerator(100*20,1,math.ceil(nodes[i].getPacInterval())):
			e = initPacket(t,i,numOfNodes)
			eventList.append(e)


	min_t  = 0

	data = []
	for i in range(numOfNodes):
		dataEach = []
		data.append(dataEach)

	while True:
		if min_t%1000 < 0.15:
			for i in range(numOfNodes-1):
				data[i].append(nodes[i].getPacInterval())
		if not eventList:
			break
		elif min_t > nodes[0].getPacInterval()*100:
			break
		else:
			min_index, min_t = min(enumerate(e.time for e in eventList),key=operator.itemgetter(1))
			newList = action(eventList[min_index],nodes)
			eventList.pop(min_index)
			for n in newList:
				eventList.append(n)
	
	#for d in data:
	#	writeResult(d,'result.csv')

	statSuc = []
	statAll = []
	


	for i in range(numOfNodes-1):
		#nodes[i].setPacInterval((60+j*20)*20)
		yes,num = nodes[i].getPacStat()
		statSuc.append(yes)
		statAll.append(num)
		#print nodes[i].getDelayStat()
		#nodes[i].printEnergyStat()
		print nodes[i].getChannelIndicators()
		#print nodes[i].getPacInterval()
	#print nodes[1].getPacInterval()
	#print sum(statSuc)/float(sum(statAll))
		h = float(nodes[i].getPacInterval())
		print h
	#print nodes[1].getDelayStat()
	#print sum(statSuc)/float(sum(statAll))/(nodes[1].getEnergyStat()/h)**8/h # 10000 is just to amplify the num
	return (sum(statSuc)/float(sum(statAll)))**1/(nodes[1].getDelayStat())**2/h 

def writeResult(result,fileName):
	with open(fileName, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for i in result:
			writer.writerow(i)

u = []
overall = []
for i in range(1):
	for j in range(1):
		dataRate = (1000+15*i)*20
		u.append(runSimulation(dataRate))
		#print u[-1]
	print sum(u)/len(u)
	overall.append(sum(u)/len(u))


	
	


