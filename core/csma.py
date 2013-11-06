class csma(object):
	channelOccupy = {}
#	eventSeq = []

	def sendCSMA(self,data,packetLength,curTime,colFlag):
		if self.carrierSensing(curTime):
			if self.carrierSensing(curTime + 1):
				for i in range(packetLength):
					csma.channelOccupy[curTime+2+i] = 1
				if colFlag == 0:
					return 'suc'
				else:
					return 'col'
			else:
				return 'c2'
		else:
			return 'c1'

	def carrierSensing(self,curTime):
		if curTime in csma.channelOccupy:
			return False
		else:
			return True

	def seqSorted(self):
		csma.eventSeq.sort()

