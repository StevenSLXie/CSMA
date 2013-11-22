def recvPhy(src,nodes,model):
	count = 0
	for n in nodes:
		if n.getTXPower() > 0:
			count += 1

	if count != 1:
		return False
	else:
		return True
