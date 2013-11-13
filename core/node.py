import random
from csma import csma
import numpy


class node(object):

	def __init__(self,i):
# curTime is the node's own clock;
		self.curTime = 0
# the following are the CSMA parameters
		self.BACKOFFLIMIT = 3
		self.MINBE = 3
		self.MAXBE = 5
		self.backoffCount = 0
		self.notInitialFlag = True  # to flag a new transmission
# the following are data
		self.data = 'Sample String.'
		self.packetLength = 3
# the following are some stat
		self.packetStat = {}
		self.busyChannel = {}
		self.transmissionCount = 0
		self.delayStat = {}
# the following are power para.
		self.curPower = 50
		self.energy = 0
		self.lastTime = 0  # last time instant when power level changes
		self.powerTX = 50
		self.powerSLEEEP = 1
		self.powerRX = 40
		self.powerSENSE = 25
		self.powerIDLE = 15

# the following are delay para
		self.packetStartTime = 0
		self.packetEndTime = 0

		self.localNodeOccupy = {}
		self.protocol = csma()
		self.ID = i

# for the sink node
		self.dataReceived = 'Good'

	def senderPacketGenerator(self):
		seq = numpy.random.poisson(80,100)
		timeSum = random.randint(0,100)
		time = []
		for i in range(len(seq)):
			timeSum = timeSum + seq[i]
			time.append(timeSum)

		for t in time:
			self.updateLocalChannel(t,1)
		

	def channelSensing(self,time):
		if self.backoffCount == 0 and self.notInitialFlag:
			self.packetStartTime = time # record the start time of the delay
#		print self.packetStartTime
			nextTime = random.randint(0,2**self.MINBE-1)+1
			self.updateLocalChannel(time + nextTime,1)
			self.notInitialFlag = False
			return 
			
		senseResult = self.protocol.getChannelState(time)
		print senseResult,self.ID,time,self.backoffCount
		if senseResult is 'CCA1' or senseResult is 'CCA2':
			self.backoffCount = self.backoffCount + 1
			if self.backoffCount <= self.BACKOFFLIMIT:
				nextTime = random.randint(0,2**min(self.MINBE + self.backoffCount,self.MAXBE)-1)+1
				if senseResult == 'CCA1':
					self.updateLocalChannel(time + nextTime,1)
				elif senseResult == 'CCA2':
					self.updateLocalChannel(time + nextTime + 1,1)
			else:
				self.notInitialFlag = True
				self.packetStat[self.transmissionCount] = 0
				self.delayStat[self.transmissionCount] = 10000000000
				self.transmissionCount = self.transmissionCount + 1
				self.backoffCount = 0				
		elif senseResult is 'IDLE':
			self.backoffCount = 0
#	self.updateLocalChannel(time+2,2)  # after 2 CCA
			self.sendingData(time+2)

	def sendingData(self,time):
#	print 'Sending...'
		self.protocol.sendingData(time,self.ID,self.packetLength)
		self.updateLocalChannel(time+self.packetLength,3)  # +1 for inter frame spacing.

	def waitingACK(self,time):
		ACKResult = self.protocol.getACK(time)
		print ACKResult
		if ACKResult == 'Suc':
			self.packetStat[self.transmissionCount] = 1
			self.delayStat[self.transmissionCount] = time-1-self.packetStartTime # -1 is to delete the time for ACK
		elif ACKResult == 'Fail':
			self.packetStat[self.transmissionCount] = 0	
			self.delayStat[self.transmissionCount] = 10000000000
		self.transmissionCount = self.transmissionCount + 1
		self.notInitialFlag = True

# for the sink node. Here assume data arrive in no time.
	def receiveData(self,time,packetLength,threshold = 100):
		self.dataReceived = self.protocol.receiveData(time,packetLength,threshold)
#	print self.dataReceived
		if self.dataReceived == 'Suc' or self.dataReceived == 'Fail':
			for i in range(packetLength):
				del self.localNodeOccupy[time+i]
			self.protocol.sendingACK(time+packetLength,self.dataReceived)
		elif self.dataReceived == 'ACK':
			del self.localNodeOccupy[time]

	def sendingACK(self,time):
		self.protocol.sendingACK(time,self.dataReceived)			
			
			
	def sinkPacketGenerator(self,span):
		for i in range(span):
			self.updateLocalChannel(i,0)


	def updateLocalChannel(self,time,flag):
	# flag 0: receiving data
	# flag 1: sensing channel;
	# flag 2: sending data;
	# flag 3: waiting for ACK
	# flag 4: sending ACK
		self.localNodeOccupy[time] = flag

	def getLocalChannel(self):
		return self.localNodeOccupy

	def getCurrentAction(self,time):
		return self.localNodeOccupy[time]

	def changePower(self,power,time):
		self.power = power
		self.lastTime = time

	def updateEnergy(self,power,time):
		self.energy = self.energy + self.power *(time-self.lastTime)
#self.lastTime = time

	def updateCurTime(self,time):
		self.curTime = time

	def getCurTime(self):
		return self.curTime
	

	def showResult(self):
		if self.ID != 9:
			print sum(self.packetStat.values()),sum(self.delayStat.values())%100000/float(sum(self.packetStat.values()))

	
#implement a energy module
#implement a time-record module.

# depends on how the delay is defined. May get different result. In this case, delay is defined as from the moment the packet is in the queue to the moment that the packet has reached the des, not counting the time taken for ACK. But only successful packets will be recorded.		

	

				
			

			
				
				
				



