def optimization(x,y,pacInterval,method):
	# x is the busy channel prob
	# y is the ack fail prob
	# pacInterval, the current 
	# method is the optimization method used.
	# 1. the pre-defined optimum beta
	# 2. return the original data arrival rate (no optimization)
	# to be continued
	beta = 0.36 # in terms of utility function
	step = 20*20
	if method == 1:
		if abs(x-beta) < 0.0001:
			return pacInterval  # remain the current data rate unchanged.
		elif x < beta:
			return max(pacInterval - step,500) # the traffic is light. can increase the data arrival rate
		elif x > beta:
			return max(pacInterval + step,500) # the traffic is heavy. should decrease the data arrival rate
	elif method == 2:
		return pacInterval
	# the problem is that the algorithm will not always converge to the same value
		
