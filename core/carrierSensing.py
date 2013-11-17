def carrierSensing(i,status,nodes):
	power = 0 
	NOISE = 0
	THRESHOLD = 5  # for the time being
	if status == 'start':
		for n in nodes:
			if i == n.getID():
				continue
			else:
				power += n.getTXPower()
		if power+NOISE > THRESHOLD:
			return False
		else:
			return True

	elif status == 'end':
		for key in nodes[i].getCCAResult():
			power += nodes[i].getCCAResult()[key]

		if power+NOISE > THRESHOLD:
			return False
		else
			return True
