import numpy as np
import pylab as pl
import csv
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
from operator import add

def plotFigure(argv,sel):
	if argv == 1:
	# Illustrate the delay and bandwidth usage.
		x = [(i*200+1000) for i in range(10)]
		x.reverse()
		y1 = []
		y2 = []
		with open('/Users/xingmanjie/Applications/Python/CSMA/core/data/d1.csv','rb') as csvfile:
			f = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in f:
				print row
				y1.append(float(row[0])*60)
				y2.append(float(row[1]))
		y1.reverse()
		y2.reverse()
		print x
		print y1
		print y2

		host = host_subplot(111, axes_class=AA.Axes)
		plt.subplots_adjust(right=0.75)
		par1 = host.twinx()

		host.set_xlim(800,3000)
		host.set_ylim(0,0.0005*60)

		host.set_xlabel('Data Arrival Interval/ symbols')
		host.set_ylabel('Bandwidth Usage')
		par1.set_ylabel('Delay/ symbols')

		p1, = host.plot(x,y1,'bo-',label='Effective Bandwidth Usage Per Node')
		p2, = par1.plot(x,y2,'rv--',label='Average Packet Delay')

		par1.set_ylim(400,1000)

		host.legend()

		host.axis["left"].label.set_color(p1.get_color())
		par1.axis["right"].label.set_color(p2.get_color())
		
		plt.draw()
		plt.show()
	elif argv == 2:
		# 2.1 shows the case for all nodes and 2.2 for average.
		# when new nodes join in and old nodes quit.
		y = []
		with open('/Users/xingmanjie/Applications/Python/CSMA/core/data/d2.csv','rb') as csvfile:
			f = csv.reader(csvfile, delimiter=' ', quotechar='|')
			for row in f:
				y.append([float(i)*4/250.0 for i in row])
		time = []
		with open('/Users/xingmanjie/Applications/Python/CSMA/core/data/d2_time.csv','rb') as csvfile:
			f2 = csv.reader(csvfile, delimiter=' ', quotechar='|')
			for t in f2:
				for ele in t:
					time.append(float(ele)*4/250)

		#for r in y:
		#x = np.linspace(0,1000*len(y[0]),len(y[0]))
		if sel == 1:
			#plt.plot(time,y[7])
			#plt.plot(time,y[32])
			for r in y[0:-1]:
				plt.plot(time,r)
			plt.xlim(0,13000)
			plt.ylim(0,520)
		else:
			temp = [0]*len(y[0])
			for r in y[0:10]:
				temp = map(add,temp,r)
			temp = [i/float(len(y[0:10])) for i in temp]
			plt.plot(time,temp,'b-',label='Group 1 Nodes')

			temp = [0]*len(y[0])
			for r in y[10:-1]:
				temp = map(add,temp,r)
			temp = [i/float(len(y[10:-1])) for i in temp]
			plt.xlim(0,12500)
			plt.ylim(0,150)
			plt.plot(time,temp,'r--',label='Group 2 Nodes')

			plt.legend()
			
		#plt.xlim(0,1000*250/4)
		#plt.ylim(0,300)
		plt.xlabel('Time/ms')
		plt.ylabel('Data Arrival Interval/ms')
		#axis([0,520,0,250])
		plt.draw()
		plt.show()

		
plotFigure(2,2)		



