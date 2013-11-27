import wx
from source import source
from event import event
from action import action
from pacGenerator import pacGenerator
import math
import operator
from initPacket import initPacket
import time
import random


class zigbeeNode(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,None,-1,'Zigbee Node Panel',size=(500,400))
		panel = wx.Panel(self,-1)
		# The following texts are for diplaying real-time data.
		self.displayData = [['Time','0',(125,-1),'s'],
					   ['Average Delay','0',(125,-1),'ms'],
					   ['Average Packet Suc','20',(125,-1),'%'],
					   ['Battery State','100',(125,-1),'%']]
		self.displayBuilder(self.displayData,panel)

		# The following buttons are for controlling settings
		self.controlData = [['Start Config',self.onStartConfig],
							['Run',self.onRun],
							['Pause',self.onPause],
							['Exit',self.onExit]]

		self.controlBuilder(self.controlData,panel)

		# The following texts are for parameter settings
		self.settingData = [['Coordinate X','10',(35,-1),'m'],
							['Coordinate Y','10',(35,-1),'m'],
							['Data Arriv Rate','100',(35,-1),'/slots'],
							['Back off Limit','4',(35,-1),'times'],
							['Retry Limit','3',(35,-1),'times'],
							['TX Power','10',(35,-1),'mW']]
		self.settingBuilder(self.settingData,panel)

		# The following are timer settings
		#self.timer = wx.Timer(self,id=1)
		#self.Bind(wx.EVT_TIMER,self.update,self.timer)

		# The following defines some variables
		self.nodes = []
		self.eventList = []

	def displayBuilder(self,data,panel):
		self.displayTitleLabel = wx.StaticText(panel,-1,'Real-time Performance Metrics',pos=(220,5))
		yPos = 30
		self.displayNameLabel = []
		self.displayText = []
		self.displayUnitLabel = []
		for d in data:
			xPos = 200
			self.displayNameLabel.append(wx.StaticText(panel,-1,d[0],pos=(xPos,yPos)))
			xPos = 330
			self.displayText.append(wx.StaticText(panel,-1,d[1],pos=(xPos,yPos),size=d[2]))
			xPos += self.displayText[0].GetSize().width
			self.displayUnitLabel.append(wx.StaticText(panel,-1,d[3],pos=(xPos,yPos)))
			yPos += self.displayUnitLabel[0].GetSize().height*1.2

	def controlBuilder(self,data,panel):
		self.controlTitleLabel = wx.StaticText(panel,-1,'Control Panel',pos=(40,5))
		yPos = 25
		self.ctrlButton = []
		i = 0
		for d in data:
			xPos = 20
			self.ctrlButton.append(wx.Button(panel, id=-1, label=d[0],pos=(xPos, yPos), size=(100, 28)))
			self.ctrlButton[i].Bind(wx.EVT_BUTTON,d[1])
			yPos += self.ctrlButton[i].GetSize().height*0.9
			i += 1

	def settingBuilder(self,data,panel):
		self.settingNameLabel = []
		self.settingText = []
		self.settingUnitLabel = []
		yPos = 150
		for d in data:
			xPos = 20
			self.settingNameLabel.append(wx.StaticText(panel,-1,d[0],pos=(xPos,yPos)))
			xPos = 120
			self.settingText.append(wx.TextCtrl(panel,-1,d[1],pos=(xPos,yPos),size=d[2]))
			xPos += self.settingText[0].GetSize().width
			self.settingUnitLabel.append(wx.StaticText(panel,-1,d[3],pos=(xPos,yPos)))
			yPos += self.settingUnitLabel[0].GetSize().height*1.1

		self.settingButton = wx.Button(panel,-1,'Set Para',pos=(25,270),size=(100,28))
		self.settingButton.Bind(wx.EVT_BUTTON,self.onSettingParameters)



	def onStartConfig(self,event):
		numOfNodes = 10
		for i in range(numOfNodes):  # initialize nodes
			argv = {}
			argv['ID'] = i
			argv['src'] = i
			argv['des'] = numOfNodes - 1
			n = source(argv)
			self.nodes.append(n)

		for i in range(numOfNodes-1):  # the last node as the sink
			for t in pacGenerator(100*20,1,math.ceil(self.nodes[i].getPacInterval()/3)):
				e = initPacket(t,i,numOfNodes)
				self.eventList.append(e)

		print 'Start Config'


	def onRun(self,event):
		min_t  = 0
		i = 0
		while True:
			i += 1
			yes,num = self.nodes[0].getPacStat()
			if num != 0:
				energy = self.nodes[0].getEnergyStat()
				energy /= 10  # /1000*100
				delay = self.nodes[0].getDelayStat()
				rate = str(yes/float(num)*100)
				#self.timer.Start(500)
				self.displayText[0].SetLabel(str(min_t*4/float(250000)))
				self.displayText[1].SetLabel(str(delay*4/float(250)))
				self.displayText[2].SetLabel(rate)
				self.displayText[3].SetLabel(str(energy))
				wx.Yield()

			#self.timer.Start(100)
			if not self.eventList:
				break
			elif min_t > self.nodes[0].getPacInterval()*200:
				break
			else:
				min_index, min_t = min(enumerate(e.time for e in self.eventList),key=operator.itemgetter(1))
				newList = action(self.eventList[min_index],self.nodes)
				self.eventList.pop(min_index)
			for n in newList:
				self.eventList.append(n)

		print 'Run'

	def onPause(self,event):
		print 'Pause'

	def onExit(self,event):
		print 'Exit'

	def onSettingParameters(self,event):
		dataRate = int(self.settingText[2].GetValue())*20
		backoffLimit = int(self.settingText[3].GetValue())
		retryLimit = int(self.settingText[4].GetValue())
		txPower = int(self.settingText[5].GetValue())

		print dataRate,backoffLimit,retryLimit

		for i in range(len(self.nodes)-1):
			self.nodes[i].setPacInterval(dataRate)
			self.nodes[i].setBOLimit(backoffLimit)
			self.nodes[i].setRTLimit(retryLimit)
		print 'Setting Para'
	
	def update(self,event):
		#yes,num = self.nodes[0].getPacStat()
		#if num != 0:
		#	print 'enter'
		#	rate = str(yes/float(num))
#	#self.timer.Start(100)
#			self.displayText[1].SetLabel(rate)
		print time.ctime()
		
if __name__ == '__main__':
	app = wx.App()
	frame = zigbeeNode()
	frame.Show()
	app.MainLoop()
