from event import event
import random
from source import source
import sys
import copy
from carrierSensing import carrierSensing
from recvPhy import recvPhy
from initPacket import initPacket
from optimization import optimization

def action(curEvent,nodes):
	BACKOFF_PERIOD = 20
	CCA_TIME = 8
	TX_TURNAROUND = 12
	ACK_TIME = 1  #12
	TX_TIME_DATA = 60
	TX_TIME_ACK = 19  #22
	ACK_WAIT = 60

#	pacInterval = random.randint(pacInterval - 100,pacInterval + 100)

	arg = curEvent.actType
	i = curEvent.src
	t = curEvent.time
	des = curEvent.des

	newList = []
	nodes[i].updateEnergy(t)

	if arg == 'sendMac':

		#nodes[i].updateEnergy(t)
		nodes[i].setPower('idle')
		
		new = copy.copy(curEvent)
		new.time = t
		new.actType = 'backoffStart'
		newList.append(new)

		nodes[i].timeStamping(t,'start')  # record the start of a packet

	elif arg == 'backoffStart': # the start of the WHOLE backoff process, boCount = 0

		nodes[i].setPower('idle')
		nodes[i].setCW(2)
		nodes[i].setBOCount(0)
		minBE,maxBE = nodes[i].getBE()
		nodes[i].setBOExponent(minBE)

		new = copy.copy(curEvent)
		new.time = t
		new.actType = 'backoff'
		newList.append(new)
	
	elif arg == 'backoff':

		nodes[i].setPower('idle')
		new = copy.copy(curEvent)
		tmp = random.randint(0,2**nodes[i].getBOExponent()-1)
		new.time = t + tmp*BACKOFF_PERIOD
		new.actType = 'ccaStart'
		newList.append(new)

	elif arg == 'ccaStart':
		
		nodes[i].setPower('sense')
		if carrierSensing(i,'start',nodes):
		#	print 'channel start is idle'
			new = copy.copy(curEvent)
			new.time = t + CCA_TIME
			new.actType = 'ccaEnd'
			nodes[i].setCCA(0)
			newList.append(new)
		else:
			# channel is busy
			#print 'channel start is busy'
			new = copy.copy(curEvent)
			new.time = t + CCA_TIME
			new.actType = 'ccaEnd'
			nodes[i].setCCA(1)
			newList.append(new)

	elif arg == 'ccaEnd':

		nodes[i].setPower('idle')
		if carrierSensing(i,'end',nodes) and nodes[i].getCCA() == 0:
			#print 'channel end is idle'
			nodes[i].setCW(-1)
			if nodes[i].getCW() == 0:
				# channel is idle for 2 consecutive CCA
				nodes[i].updateBOStat('idle')
				new = copy.copy(curEvent)
				new.time = t + TX_TURNAROUND
				new.actType = 'sendPhy'
				newList.append(new)
				nodes[i].setCW(2)

			else:
				new = copy.copy(curEvent)
				new.time = t + TX_TURNAROUND
				new.actType = 'ccaStart'
				newList.append(new)

		else:
#print 'channel end is busy'
			#channel is busy
			nodes[i].setBOCount(1)
			nodes[i].updateBOStat('busy')
			minBE,maxBE = nodes[i].getBE()
			nodes[i].setBOExponent(min(nodes[i].getBOExponent()+1,maxBE))
			if nodes[i].getBOCount() > nodes[i].getBOLimit():
				# for now assume that the interval between 2 packets is large enough
				# so no need to consider other packets in queue
				# return an empty list to indicate mission ending.
#		print  nodes[i].getBOCount() 
#		print 'Exceeds backoff limit...'
				
				nodes[i].timeStamping(t,'end')    # can add 100000000 to indicate failure.

				# schedule new packet transmission.
				if t < 5000*20:
					temp = nodes[i].getPacInterval()
					#print temp
					#print nodes[i].getChannelIndicators()
				else:
					#if i == 0:
						#print nodes[i].getChannelIndicators()
					x,y = nodes[i].getChannelIndicators()
					temp = optimization(x,y,nodes[i].getPacInterval(),2)
					nodes[i].setPacInterval(temp)
				new = initPacket(nodes[i].getPacStart()+random.randint(temp-50,temp+50),i,len(nodes))
				newList.append(new)


				nodes[i].updateDelayStat()
				nodes[i].updatePacStat(0)
				nodes[i].setBOCount(0)
				nodes[i].setRTCount(0)
			else:
#	new = event(curEvent)
				new = copy.copy(curEvent)
				new.time = t + 0.1
				new.actType = 'backoff'
				newList.append(new)
				nodes[i].setCCA(0)

	elif arg == 'sendPhy':
		
		nodes[i].setPower('tx')
		if curEvent.pacType == 'data':
			tx_time = TX_TIME_DATA
		elif curEvent.pacType == 'ack':
			tx_time = TX_TIME_ACK
		else:
			print 'no such tx time....'
			sys.exit(0)
		
		#update the power
		nodes[i].setTXPower(5)
		nodes[i].setPower('tx')
		# implement the CCA information
		for n in nodes:
			if i == n.getID():
				continue
			else:
				n.setCCAResult(i,nodes[i].getTXPower())

		new1 = copy.copy(curEvent)
		new1.src = des
		new1.des = i
		new1.actType = 'recvPhy'
		new1.time = t + tx_time
		newList.append(new1)

		new2 = copy.copy(curEvent)
		new2.time = t + tx_time + 0.5
		new2.actType = 'sendPhyFinish'
		newList.append(new2)

	elif arg == 'sendPhyFinish':
	# set up the transmitter.
		nodes[i].setPower('sleep')
		nodes[i].setTXPower(0)
		nodes[i].setPower('rx')

		for n in nodes:
			if i == n.getID():
				continue
			else:
				n.setCCAResult(i,nodes[i].getTXPower())

		
	elif arg == 'timeoutAck':

		nodes[i].setPower('sleep')
		nodes[i].setRTCount(1)
		nodes[i].updateTRYStat('fail')
		if nodes[i].getRTCount() > nodes[i].getRTLimit():
			#transmission failed.
			#print arg,'Exceed retry limit....'
			nodes[i].timeStamping(t,'end')

			# schedule new packet transmission
			if t < 5000*20:
				temp = nodes[i].getPacInterval()
				#print temp
				#print nodes[i].getChannelIndicators()
			else:
				#if i == 0:
				#		print nodes[i].getChannelIndicators()
				x,y = nodes[i].getChannelIndicators()
				temp = optimization(x,y,nodes[i].getPacInterval(),2)
				nodes[i].setPacInterval(temp)

			new = initPacket(nodes[i].getPacStart()+random.randint(temp-50,temp+50),i,len(nodes))
			newList.append(new)

			nodes[i].updateDelayStat()
			nodes[i].updatePacStat(0)
			nodes[i].setBOCount(0)
			nodes[i].setRTCount(0)

		else:
			#print arg,'packet collision'
			new = copy.copy(curEvent)
			new.actType = 'backoffStart'
			new.time = t + 0.1
			newList.append(new)

	elif arg == 'recvPhy':
		nodes[i].setPower('rx')
		model = 'ch_model'
		probRecv = recvPhy(i,nodes,model)
		#print probRecv, curEvent.pacType,nodes[i].BOCount,i
		if probRecv:
			if curEvent.pacType == 'ack':
				new = copy.copy(curEvent)
				new.time = t + 0.1
				new.actType = 'recvMac'
				newList.append(new)
			else:
				new = copy.copy(curEvent)
				new.time = t
				new.actType = 'recvMac'
				newList.append(new)
		else:
			if curEvent.pacType == 'ack':
				# nodes failed to receive ack.
				new = copy.copy(curEvent)
				new.time = t + 0.1
				new.actType = 'timeoutAck'
				newList.append(new)
			elif curEvent.pacType == 'data':
				new = copy.copy(curEvent)
				new.time = t + 0.1
				new.src = des
				new.des = i
				new.actType = 'timeoutAck'
				newList.append(new)

	elif arg == 'recvMac':
		nodes[i].setPower('idle')
		if curEvent.pacType == 'data':
			if curEvent.pacAckReq:
				new = copy.copy(curEvent)
				new.time = t + ACK_TIME  # t_ack
				new.actType = 'sendPhy'
				new.pacType = 'ack'
				new.pacAckReq = False
				# need check the following
				new.des = curEvent.des
				new.src = curEvent.src

				# here can mark the receiving of the data
				newList.append(new)
		elif curEvent.pacType == 'ack':
			# packet successfully sent and recieve right ack
			nodes[i].updateTRYStat('suc')
			nodes[i].timeStamping(t,'end')
			# to schedule next packet transmission. When t is small, channel indicators are not stable.
			if t < 5000*20:
				temp = nodes[i].getPacInterval()
				#print temp
				#print nodes[i].getChannelIndicators()
			else:
				#if i == 0:
				#		print nodes[i].getChannelIndicators()
				x,y = nodes[i].getChannelIndicators()
				temp = optimization(x,y,nodes[i].getPacInterval(),2)
				nodes[i].setPacInterval(temp)

			new = initPacket(nodes[i].getPacStart()+random.randint(temp-50,temp+50),i,len(nodes))
			newList.append(new)

			nodes[i].updateDelayStat()
			nodes[i].updatePacStat(1)
			nodes[i].setRTCount(0)
			nodes[i].setBOCount(0)

	return newList
