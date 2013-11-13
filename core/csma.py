class csma(object):
	channelOccupy = {}
#	eventSeq = []

	def carrierSensing(self,curTime):
		if curTime in csma.channelOccupy:
			return False
		else:
			return True

	def getChannelState(self,time):
		if self.carrierSensing(time):
			if self.carrierSensing(time+1):
				return 'IDLE'
			else:
				return 'CCA2'
		else:
			return 'CCA1'

	def sendingData(self,time,data,packetLength):
		for i in range(packetLength):
			if time+i in csma.channelOccupy:
				csma.channelOccupy[time+i] = csma.channelOccupy[time+i]+200*data
			else:
				csma.channelOccupy[time+i] = data
#	for i in range(3):
#			print csma.channelOccupy[time+i],time+i

	def getACK(self,time):
		if time not in csma.channelOccupy:
#		print 'enter fail'
			return 'Fail'
		elif csma.channelOccupy[time] == 1111:
			return 'Suc'
		else:
			return 'Fail'

# for the sink node			
	def receiveData(self,time,packetLength,threshold):
		flag = 0
#	print time
		if time not in csma.channelOccupy:
			return 'Idle'
		elif csma.channelOccupy[time] == 1111 or csma.channelOccupy[time] == 1010:
#elif csma.channelOccupy[time] > 1000:
			return 'ACK'
		elif csma.channelOccupy[time] > 1000:
			return 'Fail'
		else:
			for i in range(packetLength):
				print csma.channelOccupy[time+i],i,time+i
				if csma.channelOccupy[time+i] > threshold:
					flag = 1
					break
#		print flag
		if flag == 0:
#			print 'Enter Suc'
			return 'Suc'
		elif flag == 1:
			return 'Fail'

	def sendingACK(self,time,result):
		if result == 'Suc':
			csma.channelOccupy[time] = 1111
		elif result == 'Col':
			csma.channelOccupy[time] = 1010
		


		

	def seqSorted(self):
		csma.eventSeq.sort()
# when the node first sense, he may not understand that other nodes, whose ID are after it, are sending
