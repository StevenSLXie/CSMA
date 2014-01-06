import math
def optimization(x,y,pacSucRate,pacInterval,method):
	# x is the busy channel prob
	# y is the ack fail prob
	# pacInterval, the current 
	# method is the optimization method used.
	# 1. the pre-defined optimum beta
	# 2. return the original data arrival rate (no optimization)
	# 3. pricing
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
	elif method == 3:
		u = 0
		lamb = 20
		best = -1000
		L = 4
		m = 4
		#for h in range(40,500):
		#	u = pacSucRate/h - 4*lamb*(1-x**5)/h**2
			#print pacSucRate
		#	if u > best:
		#		best = u
		#		pacInterval = h
		if pacSucRate < 0.1:
			pacSucRate = 0.1
		pacInterval = 2*L*lamb*(1-x**(m+1))/(pacSucRate)  #derivative for quadratic function
		#pacInterval = math.ceil(pacInterval)
		u = pacSucRate/(pacInterval+0.01) - 4*lamb*(1-x**5)/(pacInterval+0.01)**2
		#print pacInterval,u
		#print x,y
		return math.ceil(pacInterval*20)


		
	
