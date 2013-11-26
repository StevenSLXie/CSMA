import wx

class zigbeeNode(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,None,-1,'Zigbee Node Panel',size=(500,400))
		panel = wx.Panel(self,-1)
		# The following texts are for diplaying real-time data.
		self.displayData = [['Average Dealy','1.2',(125,-1),'ms'],
					   ['Average Packet Loss','20',(125,-1),'%'],
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

	def displayBuilder(self,data,panel):
		displayTitleLabel = wx.StaticText(panel,-1,'Real-time Performance Metrics',pos=(220,5))
		yPos = 30
		displayNameLabel = []
		displayText = []
		displayUnitLabel = []
		for d in data:
			xPos = 200
			displayNameLabel.append(wx.StaticText(panel,-1,d[0],pos=(xPos,yPos)))
			xPos = 330
			displayText.append(wx.TextCtrl(panel,-1,d[1],pos=(xPos,yPos),size=d[2]))
			xPos += displayText[0].GetSize().width
			displayUnitLabel.append(wx.StaticText(panel,-1,d[3],pos=(xPos,yPos)))
			yPos += displayUnitLabel[0].GetSize().height*1.2

	def controlBuilder(self,data,panel):
		controlTitleLabel = wx.StaticText(panel,-1,'Control Panel',pos=(40,5))
		yPos = 25
		ctrlButton = []
		i = 0
		for d in data:
			xPos = 20
			ctrlButton.append(wx.Button(panel, id=-1, label=d[0],pos=(xPos, yPos), size=(100, 28)))
			ctrlButton[i].Bind(wx.EVT_BUTTON,d[1])
			yPos += ctrlButton[i].GetSize().height*0.9
			i += 1

	def settingBuilder(self,data,panel):
		settingNameLabel = []
		settingText = []
		settingUnitLabel = []
		yPos = 150
		for d in data:
			xPos = 20
			settingNameLabel.append(wx.StaticText(panel,-1,d[0],pos=(xPos,yPos)))
			xPos = 120
			settingText.append(wx.TextCtrl(panel,-1,d[1],pos=(xPos,yPos),size=d[2]))
			xPos += settingText[0].GetSize().width
			settingUnitLabel.append(wx.StaticText(panel,-1,d[3],pos=(xPos,yPos)))
			yPos += settingUnitLabel[0].GetSize().height*1.1


	def onStartConfig(self,event):
		print 'Start Config'

	def onRun(self,event):
		print 'Run'

	def onPause(self,event):
		print 'Pause'

	def onExit(self,event):
		print 'Exit'

		


if __name__ == '__main__':
	app = wx.App()
	frame = zigbeeNode()
	frame.Show()
	app.MainLoop()
