import numpy
import random

def pacGenerator(poiInterval,numPac,offset):
	seq = numpy.random.poisson(poiInterval,numPac)
	timeSum = random.randint(0,offset)
	time = []
	for i in range(len(seq)):
		timeSum = timeSum + seq[i]
		time.append(timeSum)
#print time
	return time

	
