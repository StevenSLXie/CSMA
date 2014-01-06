from source import source
from action import action
from pacGenerator import pacGenerator
from event import event
import operator
from initPacket import initPacket
import math
import random
import csv
import numpy
from itertools import izip


def runSimulation(dataRate):
	numOfNodes = 41
	nodes = []
	for i in range(numOfNodes):  # initialize nodes
		argv = {}
		argv['ID'] = i
		argv['src'] = i
		argv['des'] = numOfNodes - 1
		n = source(argv)
		nodes.append(n)

	eventList = []
	#for i in range(numOfNodes-1):
	#	nodes[i].setPacInterval(dataRate)
	'''
	for i in range(numOfNodes-1):  # the last node as the sink
		if i < 5:
			for t in pacGenerator(math.ceil(nodes[i].getPacInterval()),1,2000):
				print t
				e = initPacket(t,i,numOfNodes)
				eventList.append(e)
		else:
			for t in pacGenerator(math.ceil(nodes[i].getPacInterval()),1,21000,20000):
				print t
				e = initPacket(t,i,numOfNodes)
				eventList.append(e)
	'''
	for i in range(numOfNodes-1):
		if i < 10:
			t = random.randint(1800,2200)
		else:
			t = random.randint(300000,310000)
		e = initPacket(t,i,numOfNodes)
		eventList.append(e)

	min_t  = 0

	data = []
	for i in range(numOfNodes):
		dataEach = []
		data.append(dataEach)
	time = []
	while True:
		#print min_t
		if min_t%100 < 0.15:
			print min_t
			time.append(min_t)
			for i in range(numOfNodes-1):
				data[i].append(nodes[i].getPacInterval())
		if not eventList:
			break
		elif min_t > nodes[0].getPacInterval()*200:
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
	statDelay = []
	statEnergy = []

	aveH = []
	#print 'Average Packet Delay for each node. (Unit: ms).'
	for i in range(numOfNodes-1):
		#nodes[i].setPacInterval((60+j*20)*20)

		# For Figure 1
		yes,num = nodes[i].getPacStat()
		statSuc.append(yes)
		statAll.append(num)
		statDelay.append(nodes[i].getDelayStat())
		statEnergy.append(nodes[i].getEnergyStat())
		# End

		# For Figure 2
		d = data
		e = time
		# End

		
		#print nodes[i].getDelayStat()*4/250000.0*1000
		#nodes[i].printEnergyStat()
		#print nodes[i].getChannelIndicators()
		#print nodes[i].getPacInterval()
	#print nodes[1].getPacInterval()
	#print sum(statSuc)/float(sum(statAll))
	#h = float(nodes[i].getPacInterval())/20.0
	#aveH.append(h)
	#print h
	#print 'Average Packet Sucessful Rate for each node. (%)'
	#for i in range(numOfNodes-1):
	#	yes,num = nodes[i].getPacStat()
	#	print yes/float(num)*100
	#print numpy.mean(aveH)
	#print nodes[1].getDelayStat()
	#print sum(statSuc)/float(sum(statAll))/(nodes[1].getEnergyStat()/h)**8/h # 10000 is just to amplify the num

	# the following are for Figure 1 
	a = sum(statSuc)/float(sum(statAll))/nodes[1].getPacInterval()
	b = sum(statDelay)/float(numOfNodes-1)
	c = sum(statEnergy)/float(numOfNodes-1)
	# End

	# the following are for Figure 2

	# End
	return d,e
def writeResult(result,fileName):
	with open(fileName, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for i in result:
			writer.writerow(i)


# Figure 1
'''
u = []
overall = []
repeat = 1
for i in range(1):
	temp = (0,0)
	for j in range(repeat):
		dataRate = (50+10*i)*20
		temp = (temp[0]+runSimulation(dataRate)[0],temp[1]+runSimulation(dataRate)[1])
		#temp = tupleAdd(temp,runSimulation(dataRate))
		#print temp
		#temp.append(runSimulation(dataRate))
	temp = (temp[0]/float(repeat),temp[1]/float(repeat))
	u.append(temp)  
for obj in u:
	print obj
'''
# End

# Figure 2
pacItv,time = runSimulation(1000)
with open('/Users/xingmanjie/Applications/Python/CSMA/core/data/d2.csv','wb') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for p in pacItv:
		writer.writerow(p)	
with open('/Users/xingmanjie/Applications/Python/CSMA/core/data/d2_time.csv','wb') as csvfile:
	writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(time)	

# End
	
	


