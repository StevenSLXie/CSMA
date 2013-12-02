import math
import scipy.integrate as intl
import calIntl as ci

class phyModel(object):
	def __init__(self,argv):
		self.NOISE_FIGURE = 23
		self.BW = 30*10**3
		self.PATH_LOSS_EXPONENT = 4
		self.SHADOWING_STANDARD_DEVIATION = argv['sigma']
		self.D0 = 1.0
		self.PR_DBM = 5;
		self.NOISE = 15
		self.LAMBDA = 12.5*10*(-2)
		self.PREAMBLE_LENGTH = 40
		self.FRAME_LENGTH = argv['PACKET_LENGTH'] - PREAMBLE_LENGTH
		self.DISMIN = 1
		self.DISMAX = 20
		self.NF = self.calNoiseFloor()
		self.S = [[6.0,-3.3],[-3.3 3.7]]
		self.T = self.calCovMatrix()
		self.NOISE_FLOOR = self.NF + intl.quad(ci.calC2,-2,2,args=(self.T[0][0],))
		self.OUTPUT_POWER = self.PR_DBM + intl.dblquad(ci.calC1,-2,2,-2,2,args(self.T[0][1],self.T[1][1]))
		self.DATA_RATE = argv['DATA_RATE']

		self.P_TEMP = intl.dblquad(ci.calC,self.DISMIN,self.DISMAX,-2*self.SHADOWING_STANDARD_DEVIATION,2*self.SHADOWING_STANDARD_DEVIATION,args=(self.NOISE_FLOOR,self.DATA_RATE,self.self.BW,self.PATH_LOSS_EXPONENT,self.LAMBDA,self.OUTPUT_POWER,self.NOISE,self.D0,self.PREAMBLE_LENGTH,self.FRAME_LENGTH,self.S))

		self.P = self.P_TEMP/((self.DISMAX-self.DISMIN)*4*self.SHADOWING_STANDARD_DEVIATION)
			
	def calCovMatrix(self):
		T = []
		temp = []
		temp.append(math.sqrt(self.S[0][0]))
		temp.append(self.S[0][1]/math.sqrt(self.S[0][0]))
		T.append(T)
		temp2 = []
		temp2.append(0)
		temp2.append(math.sqrt((self.S[0][0]*self.S[1][1]-self.S[0][1]**2))/self.S[0][0])
		T.append(temp2)

		return T

	def calNoiseFloor(self):
		# Boltzman Constant
		BOLTZMAN = 1.3806504*10**(-23)
		# Temperature in degree K (for 20 Degree Celcius)
		T = 300
		# Noise Floor in dBm
		noiseFloor = 10*math.log(BOLTZMAN * T * self.BW * 10**3,10) + self.NOISE_FIGURE + 1
		return noiseFloor

	def calPSR(self):
		return self.P


	


