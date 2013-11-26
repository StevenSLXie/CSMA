#!/usr/bin/env/ python

import wx

class MenuEventFrame(wx.Frame):
	def __init__(self,parent,id):
		wx.Frame.__init__(self,parent,id,'Menus',size = (300,200))
		self.panel = wx.Panel(self)
		self.button = wx.Button(self.panel,label = 'Not Over',pos = (100,15))
		self.Bind(wx.EVT_BUTTON,self.OnButtonClick,self.button)
		self.button.Bind(wx.EVT_ENTER_WINDOW,self.OnEnterWindow)
		self.button.Bind(wx.EVT_LEAVE_WINDOW,self.OnLeaveWindow)
#	menuBar = wx.MenuBar()
#		menu1 = wx.Menu()
#		menuItem = menu1.Append(-1,'&Exit...')
#		menuBar.Append(menu1,'&File')
#		self.SetMenuBar(menuBar)
#		self.Bind(wx.EVT_MENU,self.OnCloseMe,menuItem)

	def OnCloseMe(self,event):
		self.Close(True)

	def OnButtonClick(self,event):
		self.panel.SetBackgroundColour('Green')
		self.panel.Refresh()

	def OnEnterWindow(self,event):
		self.button.SetLabel('Over Me!')
		event.skip()

	def OnLeaveWindow(self,event):
		self.button.SetLabel('Not Over!')
		event.skip()


if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = MenuEventFrame(parent = None, id = -1)
	frame.Show()
	app.MainLoop()


