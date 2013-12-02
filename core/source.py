import sys
import random

class source(object):

	def __init__(self,argv):
# the first set of parameters are CSMA/CA para.
		self.BOLimit = 4 # back off limit
		self.RTLimit = 0 # retry limit
		self.minBE = 3
		self.maxBE = 5
		self.BOCount = 0
		self.RTCount = 0
		self.BOExponent = 0
		self.CW = 2   # contention window
		self.CCA = 0
		self.CCAResult = {}
		self.ID = argv['ID']
<<<<<<< HEAD

# the following are the x,y coordinate for the node.
# use the name coordinate-x(y), as x,y are already being used for busy channel/retry prob
		self.corX = 10  #unit: m
		self.corY = 10  #unit: m

=======
>>>>>>> 8c1bc2b3aca1bda3f00ab1f1346aa632dfe8f351
# the following set of para are power para
		self.powLevel = 0  # current power setting
		self.powTX = 0     # the TX power, RF power.
		self.lastPowChange = 0  # time information. record the last time that power level has been changed.
<<<<<<< HEAD
		self.energy = 0 # J

=======
		self.energy = 1000 # J
>>>>>>> 8c1bc2b3aca1bda3f00ab1f1346aa632dfe8f351
# the following are for traffic generator
		self.poiInterval = 100  # poisson interval
		self.pacNumber = 100
# the following are for packet size and data
		self.pacSize = 3    # in terms of slot
		self.pacData = argv['src']    # use node ID as the data
# the following are the node ID, destination
		self.des = argv['des']
# the following are node stat
		self.transCount = 0
		self.packetStat = {}
		self.delayStat = {}
		self.energyStat = {}
		self.BOAttemptCount = {}
		self.TRYAttemptCount = {}
		self.BOAllCount = 0
		self.TRYAllCount = 0
		self.busyChannelProb = 0.01
		self.failAckProb = 0.01
# the following are to record the start and end time for a packet
		self.timeStart = 0
		self.timeEnd = 0
<<<<<<< HEAD

# the following are for the tuning of the parameters; the old busy channel and retry prob
		self.oldX = 0
		self.oldY = 0
=======
>>>>>>> 8c1bc2b3aca1bda3f00ab1f1346aa632dfe8f351
# the following are the packet interval.
		self.pacInterval = random.randint(60,2000)*20

	def getBOCount(self):
		return self.BOCount

	def getRTCount(self):
		return self.RTCount

	def setBOCount(self,value = 1):
		if value == 1:
			self.BOCount += 1
		elif value == 0:
			self.BOCount = 0
		else:
			print 'Cannot set other values for BOCount.....'
			sys.exit(0)

	def setRTCount(self,value = 1):
		if value == 1:
			self.RTCount += 1
		elif value == 0:
			self.RTCount = 0
		else:
			print 'Cannot set other values for RTCount.....'
			sys.exit(0)

	def getBOLimit(self):
		return self.BOLimit

	def setBOLimit(self,value):
		self.BOLimit = value

	def getRTLimit(self):
		return self.RTLimit

	def setRTLimit(self,value):
		self.RTLimit = value

	def getPower(self):
		return self.powLevel

	def setPower(self,mode):
		if mode == 'sleep':
			self.powLevel = 1
		elif mode == 'sense':
			self.powLevel = 20
		elif mode == 'tx':
			self.powLevel = 50
		elif mode == 'rx':
			self.powLevel = 45
		elif mode == 'idle':
			self.powLevel = 5
		else:
			print 'No such power mode exists...'
			sys.exit(0)

	def getTXPower(self):
		return self.powTX
	
	def setTXPower(self,value):
		self.powTX = value

	def getPacket(self):
		return self.pacSize,self.pacData

	def getTransCount(self):
		return self.transCount

	def setTransCount(self):
		self.transCont += 1

	def setStat(self,statType,key,value):
		if statType == 'packet':
			self.packetStat[key] = value
		elif statType == 'delay':
			self.delayStat[key] = value
		elif statType == 'energy':
			self.energyStat[key] = value
		else:
			print 'No such stat exists'
			# do not have to quit the program as this is not critical

	def setCW(self,value):
		if value == -1:
			self.CW -= 1
		elif value == 2:
			self.CW = 2

	def getCW(self):
		return self.CW

	def setBOExponent(self,value):
		self.BOExponent = value

	def getBOExponent(self):
		return self.BOExponent

	def getBE(self):
		return self.minBE,self.maxBE

	def getCCA(self):
		return self.CCA

	def setCCA(self,value):
		self.CCA = value

	def getID(self):
		return self.ID

	def setCCAResult(self,other,value):
		self.CCAResult[other] = value

	def getCCAResult(self):
		return self.CCAResult
	
	def updatePacStat(self,value):
		self.packetStat[self.transCount] = value
		self.transCount += 1
	# there are 2 cases: 1 means get all the stat, n mean get n recent stat 
	def getPacStat(self,arg = 1):
		if arg == 1:
			return sum(self.packetStat.values()),self.transCount
		else:
			return sum(self.packetStat.values()[-arg:]),arg

	def updateDelayStat(self):
		self.delayStat[self.transCount] = self.timeEnd - self.timeStart

	def getDelayStat(self):
		return sum(self.delayStat.values())/float(len(self.delayStat.values()))
		#for v in self.delayStat.values():
		#	print self.ID,v

	def timeStamping(self,time,options):
		if options == 'start':
			self.timeStart = time
		elif options == 'end':
			self.timeEnd = time

	def getPacStart(self):
		return self.timeStart

	def updateEnergy(self,time):
		# this must be done before changing the powLevel.
		self.energy += self.powLevel*(time-self.lastPowChange)*4/250000/1000  # data rate and mW.
		self.lastPowChange = time 

	def getEnergyStat(self):
		return self.energy

	def updateBOStat(self,result):
		if result == 'busy':
			self.BOAttemptCount[self.BOAllCount] = 1
		elif result == 'idle':
			self.BOAttemptCount[self.BOAllCount] = 0

		self.BOAllCount += 1
		self.busyChannelProb = sum(self.BOAttemptCount.values())/float(len(self.BOAttemptCount))

	def updateTRYStat(self,result):
		if result == 'suc':
			self.TRYAttemptCount[self.TRYAllCount] = 0
		elif result == 'fail':
			self.TRYAttemptCount[self.TRYAllCount] = 1

		self.TRYAllCount += 1
		self.failAckProb = sum(self.TRYAttemptCount.values())/float(len(self.TRYAttemptCount))
	# there are 2 cases: 1 means get all data; n means get the recent n data
	def getChannelIndicators(self,arg=1):
		if arg == 1:
			return self.busyChannelProb,self.failAckProb
		else:
			return sum(self.BOAttemptCount.values()[-arg:])/float(arg),sum(self.TRYAttemptCount.values()[-arg:])/float(arg)

	def getPacInterval(self):
		return self.pacInterval

	def setPacInterval(self,value):
		self.pacInterval = value

	def getOldXY(self):
		return self.oldX,self.oldY

	def setOldXY(self,x,y):
		self.oldX = x
		self.oldY = y

