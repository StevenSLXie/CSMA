import sys

class source(object):

	def __init__(self,argv):
# the first set of parameters are CSMA/CA para.
		self.BOLimit = 4 # back off limit
		self.RTLimit = 3 # retry limit
		self.minBE = 3
		self.maxBE = 5
		self.BOCount = 0
		self.RTCount = 0
		self.BOExponent = 0
		self.CW = 2   # contention window
		self.CCA = 0
		self.CCAResult = {}
		self.ID = argv.ID

# the following set of para are power para
		self.powLevel = 5  # current power setting
		self.powTX = 0     # the TX power, RF power.

# the following are for traffic generator
		self.poiInterval = 100  # poisson interval
		self.pacNumber = 100

# the following are for packet size and data
		self.pacSize = 3    # in terms of slot
		self.pacData = argv.src    # use node ID as the data

# the following are the node ID, destination
		self.ID = argv.src
		self.des = argv.des

# the following are node stat
		self.transCount = 0
		self.packetStat = {}
		self.delayStat = {}
		self.energyStat = {}

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
		elif:
			print 'Cannot set other values for RTCount.....'
			sys.exit(0)

	def getBOLimit(self):
		return self.BOLimit

	def getRTLimit(self):
		return self.RTLimit

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
		elif value == 2
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

	def setCCA(self,value)
		self.CCA = value

	def getID(self):
		return self.ID

	def setCCAResult(self,other,value):
		self.CCAResult[other] = value

	def getCCAResult(self):
		return self.CCAResult
	
	


