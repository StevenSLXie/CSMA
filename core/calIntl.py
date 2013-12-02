import math
import scipy.integrate as intl

def calC(dist,shadowingStd,noiseFloor,dataRate,bandWidth,pathLossExpo,waveLength,outputPower,noise,d0,preambleLength,frameLength,S):
	RSSI = calRSSI(PrdBm,dist,waveLength,noise,pathLossExpo,shadowingStd,d0)
	ebno =  RSSIToEbN0(RSSI,codeRate,dataRate,bandWidth,noiseFloor)
	per = pError(ebno,5):
	ppr = packetCoding(per,1,preambleLength,frameLength)
	return calC


def calC1(rn1,rn2,t12,t22):
	return t12*rn1 + t22*rn2

def calC2(rn1,t11):
	return t11*rn1

def calRSSI(PrdBm,dist,waveLength,noise,pathLossExpo,shadowingStd,d0):
	PL_D0 = 20*math.log((4*3.1415926)/waveLength,10) + noise
	L = (PL_D0 + 10*pathLossExpo*math.log(dist/d0,10)) + shadowingStd
	return prdBm - L

def RSSIToEbN0(RSSI,codeRate,dataRate,bandWidth,noiseFloor):
	gain = 10*math.log(dataRate*codeRate/bandWidth,10)
	EbN0_dBm = RSSI - noiseFloor - gain
	return dBm2mW(EbN0_dBm)

def dBm2mW(EbN0_dBm):
	return 10**(EbN0_dBm/10)

def pError(snr,modulation):
	if modulation == 1:
		return 0.5*(math.exp(-0.5*snr)+Q(math.sqrt(snr)))
	elif modulation == 2:
		return Q(math.sqrt(snr/2))
	elif modulation == 3:
		return 0.5*math.exp(-0.5*snr)
	elif modulation == 4:
		return Q(math.sqrt(snr))
	elif modulation == 5:
		return Q(math.sqrt(2*snr))
	elif modulation == 6:
		return 0.5*math.exp(-snr)

def Q(x):
	return 0.5*erfc(x/math.sqrt(2))

def erfc(x):
	return 2/math.sqrt(3.1415926)*intl.quad(intlErfc,x,float('Inf'))

def intlErfc():
	return math.exp(-t**2)

def packetCoding(pe,encoding,preambleLength,frameLength):
	preseq = (1-pe)**(8*preambleLength)
	if encoding == 1:
		return preseq*((1-pe)**(8*(frameLength-preambleLength)))
	elif encoding == 2:
		return preseq*((1-pe)**(8*1.25*(frameLength-preambleLength)))
	elif encoding == 3:
		return preseq*((1-pe)**(8*2(frameLength-preambleLength)))
	elif encoding == 4:
		return ((preseq*((1-pe)**8)) + (8*pe*((1-pe)**7)))**((frameLength-preambleLength)*3)
	else:
		import sys
		print 'Encoding is incorrect.'
		sys.exit(0)



