import random
from csma import csma
import numpy


class node(object):

	def __init__(self,i):
# curTime is the node's own clock;
		self.curTime = 0
# the following are the CSMA parameters
		self.BACKOFFLIMIT = 4
		self.MINBE = 3
		self.MAXBE = 5
		self.backoffCount = 0
# the following are data
		self.data = 'Sample String.'
		self.packetLength = 3
# the following are some stat
		self.packetStat = {}
		self.busyChannel = {}
		self.transmissionCount = 0
# the following are power para.
		self.power = 50
		self.energy = 0

		self.localNodeOccupy = {}
		self.protocol = csma()
		self.ID = i

	def runNode(self,until= 10000):
		self.curTime = 0
		while self.curTime < until: 
			self.curTime = self.curTime + 1
			if self.curTime in self.localNodeOccupy:
#		if self.ID == 3:
#				print self.curTime
				self.send()

	def packetGenerator(self):
		seq = numpy.random.poisson(50,200)
		timeSum = random.randint(0,20)
		time = []
		for i in range(len(seq)):
			timeSum = timeSum + seq[i]
			time.append(timeSum)

		for t in time:
			self.updateLocalChannel(t)
		
	def send(self,time,colFlag):
		if self.backoffCount <= self.BACKOFFLIMIT:
			t = self.protocol.sendCSMA(self.data,self.packetLength,time,colFlag)
#		print t
			if t == 'suc' or t == 'col':
				self.transmissionCount = self.transmissionCount + 1
				self.curTime = self.curTime + self.packetLength - 1 # transmission takes L slots
				self.backoffCount = 0
				if t == 'col':
					self.packetStat[self.transmissionCount] = 0
				else:
					self.packetStat[self.transmissionCount] = 1					
			else:
				nextTime = random.randint(0,2**min(self.MINBE + self.backoffCount,self.MAXBE)-1)+1
				self.backoffCount = self.backoffCount + 1
				self.updateLocalChannel(time + nextTime)
#			print self.getLocalChannel()
				if t == 'c2':
					self.curTime = self.curTime + 1 # CCA takes 2 time slot
		else:
			self.packetStat[self.transmissionCount] = 0
			self.transmissionCount = self.transmissionCount + 1
			self.backoffCount = 0

	def updateLocalChannel(self,time):
		self.localNodeOccupy[time] = 1

	def getLocalChannel(self):
		return self.localNodeOccupy

	def changePower(power):
		self.power = power

	def showResult(self):
		print sum(self.packetStat.values())
#	print self.transmissionCount


#implement a energy module
#implement a time-record module.
		

	

				
			

			
				
				
				



