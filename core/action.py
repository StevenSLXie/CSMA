from event import event
import random
from source import source
import sys

def action(curEvent,nodes):
	BACKOFF_PERIOD = 20
	CCA_TIME = 8
	TX_TURNAROUND = 12
	ACK_TIME = 12
	TX_TIME_DATA = 60
	TX_TIME_ACK = 22
	ACK_WAIT = 60



	arg = curEvent.actType
	i = curEvent.src
	t = curEvent.time
	des = curEvent.des

	newList = []

	if arg == 'sendMac':
		
		new = event(curEvent)
		new.time = t + 0.1
		new.actType = 'backoffStart'
		newList.append(new)

	elif arg == 'backoffStart': # the start of the WHOLE backoff process, boCount = 0
		nodes[i].setCW(2)
		nodes[i].setBOCount(0)
		minBE,maxBE = nodes[i].getBE()
		nodes[i].setBOExponent(minBE)

		new = event(curEvent)
		new.time = t
		new.actType = 'backoff'
		newList.append(new)
	
	elif arg == 'backoff':
		new = event(curEvent)
		tmp = random.randint(0,2**nodes[i].getBOExponent()-1)
		new.time = t + tmp*BACKOFF_PERIOD
		new.actType = 'ccaStart'
		newList.append(new)

	elif arg == 'ccaStart':
		
		if carrierSensing(i,'start') == 0:
			new = event(curEvent)
			new.time = t + CCA_TIME
			new.actType = 'ccaEnd'
			nodes[i].setCCA(0)
			newList.append(new)
		else:
			# channel is busy
			new = event(curEvent)
			new.time = t + CCA_TIME
			new.actType = 'ccaEnd'
			nodes[i].setCCA(1)
			newList.append(new)


	elif arg == 'ccaEnd':

		if carrierSensing(i,'end') == 0 and nodes[i].getCCA() == 0:
			nodes[i].setCW(-1)
			if nodes[i].getCW() == 0:
				new = event(curEvent)
				new.time = t + TX_TURNAROUND
				new.actType = 'sendPhy'
				newList.append(new)

			else:
				new = event(curEvent)
				new.time = t + TX_TURNAROUND
				new.actType = 'ccaStart'
				newList.append(new)

		else:
			#channel is busy
			nodes[i].setBOCount(1)
			minBE,maxBE = nodes[i].getBE()
			nodes[i].setBOExponent(min(nodes[i].getBOExponent()+1,maxBE))
			if nodes[i].getBOCount > nodes[i].getBOLimit():
				# for now assume that the interval between 2 packets is large enough
				# so no need to consider other packets in queue
				# return an empty list to indicate mission ending.
			else:
				new = event(curEvent)
				new.time = t + 0.1
				new.actType = 'backoff'
				newList.append(new)

	elif arg == 'sendPhy':
	
		if curEvent.pacType == 'data':
			tx_time = TX_TIME_DATA
		elif curEvent.pacType == 'ack':
			tx_time = TX_TIME_ACK
		else:
			print 'no such tx time....'
			sys.exit(0)
			

		new1 = event(curEvent)
		new1.src = des
		new1.des = i
		new1.actType = 'recvPhy'
		new1.time = t + tx_time
		newList.append(new1)

		new2 = event(curEvent)
		new2.time = t + tx_time + 0.1
		new2.actType = 'sendPhyFinish'
		newList.append(new2)

		if curEvent.pacAckReq:
			new3 = event(curEvent)
			new3.time = t + tx_time + ACK_WAIT
			new3.actType = 'timeoutAck'
			newList.append(new3)

	elif arg == 'sendPhyFinish':
	# don't understand the logic. Leave it blank now.

		
	elif arg == 'timeoutAck':
		nodes[i].setRTCount(1)
		if nodes[i].getRTCount() > nodes[i].getRTLimit():
			#transmission failed.
			# need to record stat.
			# blank for now.
			
		else:
			new = event(curEvent)
			new.actType = 'backoffStart'
			new.time = t + 0.1
			newList.append(new)

	elif arg == 'recvPhy':
		model = 'ch_model'
		pr,snr = recv_phy(i,src,model)

		if snr >= rvThreshold:
			probRecv = True
		else:
			probRecv = False

		if probRecv:
			if curEvent.pacType == 'ack':
				new = event(curEvent)
				new.time = t + 0.1
				new.actType = 'recvMac'
				newList.append(new)
			elif des == i:
			# if not ack, then is the data
				new = event(curEvent)
				new.time = t
				new.actType = 'recvMac'
				newList.append(new)
		else:
			# cannot receive

	elif arg == 'recvMac':
		if curEvent.pacType == 'data':
			if curEvent.pacAckReq:
				new = event()  # brand-new pac
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
			nodes[i].setRTCount(0)

	return newList
		

		

		

		



		
		
		
		
		
