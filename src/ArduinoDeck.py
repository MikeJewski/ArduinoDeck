import wx
import wx.lib.agw.foldpanelbar as fpb
from wx.lib.agw.shapedbutton import SBitmapButton
import wx.lib.buttons as buttons
import json
from obswebsocket import obsws, requests
import os
import time
import subprocess
import serial.tools.list_ports

"""
Arduino Deck 

October 17, 2017

This is a GUI designed by MikeJewski which allows a user to edit the layout
of an Arduino running the ArduinoDeck software. This allows the user to set 
custom images, custom commands, and reorganize the layout of the touchscreen
of the ardunio device.

For information on how to setup the hardware and software for this project,
please read over the README file: 

"""
with open("Setup.txt","r") as data:
	values = data.readlines()
	for i in range(0,len(values)):
		exec(values[i] )
		
class MainPanel(wx.Panel):

#----------------------------------------------------------------------
	def __init__(self, parent):

		wx.Panel.__init__(self, parent)

		self.ButtonLayout = []
		self.ActiveAction = []
		self.ActiveOptions = []
		self.DeckState = False
		self.DeckThread = []
		self.CurrentLayout = []
		self.LayoutDir = os.getcwd()+"\\Layouts" 

		# Read the setup file, which contains information about the current layout,
		# as well as user information required for the ticker and Twitch chat. This
		# may also include social media like Twitter in the future if many people
		# inquire about it

		with open("Setup.txt","r") as data:
			values = data.readlines()
			for i in range(0,len(values)):
				exec("self." + values[i] )

		with open(self.LayoutDir+"\\"+self.CurrentLayout,"r") as json_data:
			self.ButtonLayout = json.load(json_data)

		# Setup the main splitter environment for the application
		# This will be changed to box sizers in the future, as this 
		# was written at the beginning of the project when I did not
		# understand how to use box sizers, and I am too lazy to fix this

		self.topSplitter = wx.SplitterWindow(self)
		self.vSplitter = wx.SplitterWindow(self.topSplitter)

		self.csStyle = self.csStyleSetup()

		self.ActionPanelSetup()

		self.ImageDir = os.getcwd()+"\\ArduinoDeckIcons\\"

		self.ButtonPanel = wx.Panel(self.vSplitter,-1,name="panelTwo")
		self.ButtonPanel.SetBackgroundColour("#161713")

		self.ButtonPanelSetup()

		self.OptionPanel = wx.Panel(self.vSplitter,-1,name="panelThree")
		self.OptionPanel.SetBackgroundColour("#161713")

		self.CreateStaticButtons()

		self.vSplitter.SplitHorizontally(self.ButtonPanel, self.OptionPanel)
		self.vSplitter.SetSashGravity(0.7)

		self.ActionPanel = self.panel_bar
		self.topSplitter.SplitVertically(self.vSplitter, self.ActionPanel)
		self.topSplitter.SetSashGravity(0.9)
		self.topSplitter.SetMinimumPaneSize(-1)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.topSplitter, 1, wx.EXPAND)
		self.SetSizer(sizer)

		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_CHOICE, self.OnChoice)
		self.Bind(wx.EVT_BUTTON, self.OnClick) 
		self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.LockSplitter)

		self.ActionButtons = self.TwitchButtons+self.OBSButtons+self.MediaButtons+self.BitmapButtons+self.ButtonImage+self.SystemFunctions

		for i in range(0,len(self.ActionButtons)):
			self.ActionButtons[i].SetBackgroundColour("#272822")
			self.ActionButtons[i].SetForegroundColour("#c1c1bf")
	   

	def csStyleSetup(self):
		# Style used for fold bar menu 

		csStyle = fpb.CaptionBarStyle()
		csStyle.SetFirstColour(wx.Colour("#36393e"))
		csStyle.SetSecondColour(wx.Colour("#36393e"))
		csStyle.SetCaptionColour("WHITE")
		csStyle.SetCaptionFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD))
		return csStyle

	def ButtonPanelSetup(self):

		# Setup of the buttons. Buttons are not removed, only disabled and switched to a different colour. Images used must be .bmp, 
		# I have included a quick script in the main folder (convert.py) which will convert images into .bmp, and place it into the 
		# ArduinoDeckIcons folder so that users may make their own. The image size is 58x58 .bmp 24 bit colour.

		self.padding = 70
		self.edge = 35
		bmp = wx.Bitmap(self.ImageDir+"Discord.bmp", wx.BITMAP_TYPE_ANY)

		self.Button1 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button1")

		self.Button2 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button2")

		self.Button3 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button3")

		self.Button4 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button4")

		self.Button5 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button5")

		self.Button6 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button6")

		self.Button7 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button7")

		self.Button8 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button8")

		self.Button9 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button9")

		self.Button10 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button10")

		self.Button11 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button11")

		self.Button12 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button12")

		self.Button13 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button13")

		self.Button14 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button14")

		self.Button15 = buttons.GenBitmapToggleButton(self.ButtonPanel,bitmap=bmp,size=(bmp.GetWidth()+10, bmp.GetHeight()+10),style=wx.NO_BORDER,name="Button15")


		self.BitmapButtons = [self.Button1,self.Button2,self.Button3,self.Button4,self.Button5,self.Button6,self.Button7,self.Button8,self.Button9,self.Button10,self.Button11,self.Button12,self.Button13,self.Button14,self.Button15]

		# Placement of the buttons relative to eachother

		for i in range(0,5):
			for j in range(0,3):
				num = (i)+(j*5)
				Image = self.ButtonLayout["Button"+str(num+1)]["Image"]
				bmp = wx.Bitmap(self.ImageDir+Image, wx.BITMAP_TYPE_ANY)
				self.BitmapButtons[num].SetBackgroundColour("#272822")
				self.BitmapButtons[num].SetBitmapLabel(bmp)
				self.BitmapButtons[num].SetPosition((self.edge+((bmp.GetWidth()+10)+self.padding)*i,self.edge+((bmp.GetWidth()+10)+self.padding)*j))

				self.BitmapButtons[num].Bind(wx.EVT_LEFT_DOWN, self.Move)

		self.ActiveButton = []

		bmp = wx.Bitmap(os.getcwd()+"\\SystemIcons\\"+"add.png", wx.BITMAP_TYPE_ANY)
		self.AddButton =SBitmapButton(self.ButtonPanel, wx.ID_ANY,bitmap=bmp,size=(40,40),pos=(650,400))
		self.AddID = self.AddButton.Id
		self.AddButton.SetUseFocusIndicator(False) 

	def ActionPanelSetup(self):

		#Setup of the FoldPanelBar on the right size of window

		self.panel_bar = fpb.FoldPanelBar(self.topSplitter, -1, pos=(0,0), size=(150,100),style= wx.BORDER_NONE,agwStyle=fpb.FPB_VERTICAL| fpb.FPB_SINGLE_FOLD)
		self.panel_bar.SetBackgroundColour("#161713")
		

		item = self.panel_bar.AddFoldPanel("Twitch", collapsed=True,cbstyle=self.csStyle)

		self.Sub = wx.Button(item,label="Sub Mode", name="SubMode",size=(-1,-1),style=wx.BORDER_NONE)
		self.Emote = wx.Button(item,label="Emote Mode",name="EmoteMode",size=(-1,-1),style=wx.BORDER_NONE)
		self.Follow = wx.Button(item,label="Follower Mode",name="FollowerMode",size=(-1,-1),style=wx.BORDER_NONE)
		self.Slow = wx.Button(item,label="Slow Mode",name="SlowMode",size=(-1,-1),style=wx.BORDER_NONE)
		self.Sellout = wx.Button(item,label="Commercial",name="Commercial",size=(-1,-1),style=wx.BORDER_NONE)
		self.Custom = wx.Button(item,label="Custom Message",name="CustomMessage",size=(-1,-1),style=wx.BORDER_NONE)

		self.TwitchButtons = [self.Sub,self.Emote,self.Follow,self.Slow,self.Sellout,self.Custom]

		for i in range(0,len(self.TwitchButtons)):
			self.panel_bar.AddFoldPanelWindow(item, self.TwitchButtons[i])

		item = self.panel_bar.AddFoldPanel("OBS", collapsed=True,cbstyle=self.csStyle)

		self.OBSSource = wx.Button(item,label="Toggle Source", name="ToggleSource",size=(-1,-1),style=wx.BORDER_NONE)
		self.OBSScene = wx.Button(item,label="Switch to Scene",name="ChooseScene",size=(-1,-1),style=wx.BORDER_NONE)
		self.OBSMic = wx.Button(item,label="Toggle Mic",name="Mic",size=(-1,-1),style=wx.BORDER_NONE)
		self.OBSRec = wx.Button(item,label="Start/Stop Recording",name="Rec",size=(-1,-1),style=wx.BORDER_NONE)
		self.OBSStream = wx.Button(item,label="Start/Stop Streaming",name="Stream",size=(-1,-1),style=wx.BORDER_NONE)
		
		self.OBSButtons = [self.OBSSource,self.OBSScene,self.OBSMic,self.OBSRec,self.OBSStream]

		for i in range(0,len(self.OBSButtons)):
			self.panel_bar.AddFoldPanelWindow(item, self.OBSButtons[i])

		item = self.panel_bar.AddFoldPanel("Media Keys", collapsed=True,cbstyle=self.csStyle)

		self.MediaPrev = wx.Button(item,label="Previous Track", name="PreviousTrack",size=(-1,-1),style=wx.BORDER_NONE)
		self.MediaNext = wx.Button(item,label="Next Track", name="NextTrack",size=(-1,-1),style=wx.BORDER_NONE)
		self.MediaPlayPause = wx.Button(item,label="Play/Pause", name="PlayPause",size=(-1,-1),style=wx.BORDER_NONE)
		self.MediaMute = wx.Button(item,label="Mute", name="Mute",size=(-1,-1),style=wx.BORDER_NONE)
		self.MediaStop = wx.Button(item,label="Stop", name="Stop",size=(-1,-1),style=wx.BORDER_NONE)
		self.MediaVolumeUp = wx.Button(item,label="Volume Up", name="VolumeUp",size=(-1,-1),style=wx.BORDER_NONE)
		self.MediaVolumeDown = wx.Button(item,label="Volume Down", name="VolumeDown",size=(-1,-1),style=wx.BORDER_NONE)

		self.MediaButtons = [self.MediaPrev,self.MediaNext,self.MediaPlayPause,self.MediaMute,self.MediaStop,self.MediaVolumeUp,self.MediaVolumeDown]

		for i in range(0,len(self.MediaButtons)):
			self.panel_bar.AddFoldPanelWindow(item, self.MediaButtons[i])

		item = self.panel_bar.AddFoldPanel("Button Image", collapsed=True,cbstyle=self.csStyle)

		self.Change = wx.Button(item,label="Change Image",name="ChangeImage",size=(-1,-1),style=wx.BORDER_NONE)

		self.ButtonImage = [self.Change]

		for i in range(0,len(self.ButtonImage)):
			self.panel_bar.AddFoldPanelWindow(item, self.ButtonImage[i])

		item = self.panel_bar.AddFoldPanel("System Functions", collapsed=True,cbstyle=self.csStyle)

		self.SystemHotkey = wx.Button(item,label="Set Hotkey",name="Hotkey",size=(-1,-1),style=wx.BORDER_NONE)

		self.SystemFunctions = [self.SystemHotkey]

		for i in range(0,len(self.SystemFunctions)):
			self.panel_bar.AddFoldPanelWindow(item, self.SystemFunctions[i])

	def Move(self,event):

		# Create movement of buttons when rearranging the button placements. Button follows the mouse, 
		# if user lets go of the mouse button when over another button, it will move the button to this
		# position of the ArduinoDeck

		name = event.GetEventObject().GetName()
		if(self.ButtonLayout[name]["Active"] == True):

			#Get the position of the mouse
			x,y = frame.ScreenToClient(event.GetEventObject().GetScreenPosition())
			mouse_x,mouse_y = frame.ScreenToClient(wx.GetMousePosition())

			diff_x = mouse_x-x
			diff_y = mouse_y-y

			click_down = time.time()
			held = False
			name = event.GetEventObject().GetName()

			# Setup the garbage image 

			garbage0 = wx.Bitmap(os.getcwd()+"\\SystemIcons\\"+"garbage0.bmp", wx.BITMAP_TYPE_ANY)
			garbage1 = wx.Bitmap(os.getcwd()+"\\SystemIcons\\"+"garbage.bmp", wx.BITMAP_TYPE_ANY)

			# Constants for checking states etc

			mouse_below = False
			refreshTimer = time.time()
			dc = wx.MemoryDC()
			garbage_update = False

			while wx.MouseEvent.LeftIsDown(wx.GetMouseState()):
				#If mouse has been clicked for more than 0.2 seconds, assume user it attempting to move it
				if (time.time()-click_down) > 0.2:
					#Setup for once the mouse has been confirmed to be held down
					if held==False:

						held = True

						# Create a new panel that will follow the mouse around while it is clicked down

						self.panel2 = wx.Panel(self.ButtonPanel,-1,size=(58,58),pos=(0,0))
						ImageDir = os.getcwd()+"\\ArduinoDeckIcons\\"
						bmp = wx.Bitmap(self.ImageDir+"Disabled.bmp", wx.BITMAP_TYPE_ANY)
						event.GetEventObject().SetBitmapLabel(bmp)

						# Refresh the ButtonPanel
						self.ButtonPanel.Refresh()

						bmp = wx.Bitmap(ImageDir+self.ButtonLayout[name]["Image"], wx.BITMAP_TYPE_ANY)
						imageBitmap = wx.StaticBitmap(self.ButtonPanel, wx.ID_ANY, garbage0,pos=(0,443))
						image = wx.StaticBitmap(self.panel2, wx.ID_ANY, bmp)

					# Continuously capture the users x,y positions and move the panel accordingly
					mouse_x,mouse_y = frame.ScreenToClient(wx.GetMousePosition())
					self.panel2.SetPosition((mouse_x-diff_x,mouse_y-diff_y))
					
					# If the mouse goes below the garbage line, changes the image to a red garbage can, indicating the button
					# will be removed

					if mouse_y > 443:
						if mouse_below == False:
							imageBitmap.SetBitmap(garbage1)
							refreshTimer = time.time()
							mouse_below = True
							garbage_update = True
						  
					if mouse_y <= 443:
						if mouse_below == True:
							imageBitmap.SetBitmap(garbage0)
							refreshTimer = time.time()
							mouse_below = False
							garbage_update = True
					
					# Update the panel 
					self.ButtonPanel.Update()
					
					if (garbage_update == True) & ((time.time() - refreshTimer) > 0.15):
						garbage_update = False
						refreshTimer = time.time()
						self.panel2.Refresh()

					time.sleep(0.01)

			# Once the user has let go of the mouse, destroy the panel that they were holding
			try:        
				self.panel2.Destroy()
				imageBitmap.Destroy()
			except:
				None

			# Get the x,y upon release
			new_x,new_y = frame.ScreenToClient(wx.GetMousePosition())

			# If the user was indeed holding down the mouse, and created a button, use the x,y pos after letting go
			# and swap buttons where ever it was released.

			if held == True:
				for i in range(0,5):
					for j in range(0,3):
						  num = (i)+(j*5)
						  if(new_x > (self.edge+((68)+self.padding)*i)) & (new_x < (self.edge+((68)+self.padding)*i)+58):
								if(new_y > (self.edge+((68)+self.padding)*j)) & (new_y < (self.edge+((68)+self.padding)*j)+58):
									ButtonSwitch = "Button"+str(num+1)
									placeholder = self.ButtonLayout[name]
									self.ButtonLayout[name] = self.ButtonLayout[ButtonSwitch]
									Image = self.ButtonLayout[name]["Image"]
									bmp = wx.Bitmap(self.ImageDir+Image, wx.BITMAP_TYPE_ANY)
									exec("self." + name + ".SetBitmapLabel(bmp)")

									self.ButtonLayout[ButtonSwitch] = placeholder
									Image = self.ButtonLayout[ButtonSwitch]["Image"]
									bmp = wx.Bitmap(self.ImageDir+Image, wx.BITMAP_TYPE_ANY)
									exec("self." + ButtonSwitch + ".SetBitmapLabel(bmp)")
									self.Refresh()
				
				# If it is below the garbage line, delete the button and replace the image with the default blank
				if new_y > 443:
					bmp = wx.Bitmap(self.ImageDir+"Disabled.bmp", wx.BITMAP_TYPE_ANY)
					event.GetEventObject().SetBitmapLabel(bmp)
					event.GetEventObject().Refresh()   
					self.ButtonLayout[name]["Image"] = "Disabled.bmp"
					self.ButtonLayout[name]["Action"] = None
					self.ButtonLayout[name]["Active"] = False

			Image = self.ButtonLayout[name]["Image"]
			bmp = wx.Bitmap(self.ImageDir+Image, wx.BITMAP_TYPE_ANY)
			exec("self." + name + ".SetBitmapLabel(bmp)")
			self.ButtonPanel.Refresh()
			
			# If the user did not hold down the mouse long enough to register as a hold, treat it as a click event
			if held == False:
				self.OnClick(event)

	#This entire section is a mess, I don't even want to waste my time trying to comment this. This needs a major update
	def OnClick(self,event):
		parent = event.GetEventObject().GetParent().GetName()
		name = event.GetEventObject().GetName()
		if (parent == "panel"):
			for i in range(0,len(self.ActionButtons)):
				buttonName = self.ActionButtons[i].GetName()
				if buttonName == name:
					self.ActionButtons[i].SetBackgroundColour("#40413e")
					self.ActionButtons[i].SetForegroundColour("#c1c1bf")
					self.ActiveAction = self.ActionButtons[i]
					if buttonName != "ChangeImage":
						self.ButtonLayout[self.ActiveButton.GetName()]["Action"] = {"Name":self.ActiveAction.GetName()}
					for child in self.OptionPanel.GetChildren():
						if (child in self.StaticButtons) == False:
							 child.Destroy()
					exec("self.ActiveOptions = self."+buttonName+"()")

				else:
					self.ActionButtons[i].SetBackgroundColour("#272822")


		if parent == "panelTwo":
			for i in range(0,len(self.BitmapButtons)):
				buttonName = self.BitmapButtons[i].GetName()
				try:
					if (buttonName == name) & (self.ButtonLayout[name]["Active"] == True):
						self.BitmapButtons[i].SetToggle(True)
						self.ActiveButton = self.BitmapButtons[i]
						for child in self.OptionPanel.GetChildren():
							if (child in self.StaticButtons) == False:
								child.Destroy()
						try:
							exec("self.ActiveOptions = self."+self.ButtonLayout[self.ActiveButton.GetName()]["Action"]["Name"]+"()")
							for i in range(0,len(self.OptionPanelButtons)):
								value = self.ButtonLayout[self.ActiveButton.GetName()]["Action"][self.OptionPanelButtons[i].GetName()].encode("utf-8")
								value = self.OptionPanelButtons[i].FindString(value)
								self.OptionPanelButtons[i].SetSelection(value)
								ActionName =  self.ButtonLayout[self.ActiveButton.GetName()]["Action"]["Name"].encode("utf-8")
								for j in range(0,len(self.ActionButtons)):
									if ActionName == self.ActionButtons[j].GetName():
										self.ActiveAction = self.ActionButtons[j]
										break
								self.SendEvent(self.OptionPanelButtons[i])
						except:
							try:
									self.HotKeyEnter.SetValue(' + '.join(self.ButtonLayout[self.ActiveButton.GetName()]["Action"]["Hotkey"]))
							except:
								try:
									self.Message.ChangeValue(self.ButtonLayout[self.ActiveButton.GetName()]["Action"]["Message"])
									self.Refresh()
								except:
									None
					else:
						self.BitmapButtons[i].SetToggle(False)
				except:
					None

			self.ButtonPanel.Refresh()

			if event.GetEventObject().Id == self.AddID:
				for i in range(0,len(self.BitmapButtons)):
					ButtonName = self.BitmapButtons[i].GetName()
					if self.ButtonLayout[ButtonName]["Active"] == False:
						self.ButtonLayout[ButtonName]["Active"] = True
						self.ButtonLayout[ButtonName]["Image"] = "Mic0.bmp"
						Image = self.ButtonLayout[ButtonName]["Image"]
						bmp = wx.Bitmap(self.ImageDir+Image, wx.BITMAP_TYPE_ANY)
						exec("self." + ButtonName + ".SetBitmapLabel(bmp)")
						break

			self.ButtonPanel.Refresh()

		if parent == "panelThree":
			exec("self."+name+"()")


	def SendEvent (self, mycontrol):
		cmd = wx.CommandEvent(wx.EVT_CHOICE.evtType[0])
		cmd.SetEventObject(mycontrol)
		cmd.SetId(mycontrol.GetId())
		mycontrol.GetEventHandler().ProcessEvent(cmd)

	def OnChoice(self,event):
		NewChoice = event.GetEventObject()
		Selection = NewChoice.GetString(NewChoice.GetSelection()) 
		self.ButtonLayout[self.ActiveButton.GetName()]["Action"][NewChoice.GetName()] = Selection
		if(self.ActiveAction.GetName() == "ToggleSource") & (NewChoice.GetName() == "Scene"):
			self.SourceList = self.GetSources(Selection)
			self.Source.Set(self.SourceList)

	def OnClose(self):
		try:
			self.StartStopDeck(True)
		except:
			None

	def LockSplitter(self,event):
		event.Veto()
	
	def CreateStaticButtons(self):
		self.SaveLayout = wx.Button(self.OptionPanel,-1,label="Save Layout",size=(120,20),pos=(572,8),style=wx.BORDER_NONE,name="Save")
		self.SaveLayoutAs = wx.Button(self.OptionPanel,-1,label="Save Layout As",size=(120,20),pos=(572,44),style=wx.BORDER_NONE,name="SaveAs")
		self.LoadLayout = wx.Button(self.OptionPanel,-1,label="Load Layout",size=(120,20),pos=(572,80),style=wx.BORDER_NONE,name="Load")
		self.UploadLayout = wx.Button(self.OptionPanel,-1,label="Upload Layout",size=(120,20),pos=(572,116),style=wx.BORDER_NONE,name="Upload")
		self.ToggleDeck = wx.Button(self.OptionPanel,-1,label="Start Deck",size=(120,20),pos=(572,152),style=wx.BORDER_NONE,name="StartStopDeck")

		self.StaticButtons = [self.SaveLayout,self.SaveLayoutAs,self.LoadLayout,self.UploadLayout,self.ToggleDeck]

		for i in range(0,len(self.StaticButtons)):
			self.StaticButtons[i].SetBackgroundColour("#272822")
			self.StaticButtons[i].SetForegroundColour("#c1c1bf")

	def Save(self):
		with open(self.LayoutDir+"\\"+self.CurrentLayout,'w') as json_data:
			  json.dump(self.ButtonLayout,json_data)


	def SaveAs(self):
		dirname = self.LayoutDir
		dlg = wx.FileDialog(self, "Save Layout File", dirname, "", "Layout files (json)|*.json", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

		if dlg.ShowModal() == wx.ID_CANCEL:
			return
		else:
			sel_dir = dlg.GetDirectory()
			if sel_dir != dirname:
				wx.MessageBox('Please save the file in the correct directory', 'Error', wx.OK | wx.ICON_ERROR)
			else:
				pathname = dlg.GetPath()
				try:
					with open(pathname, 'w') as json_data:
						json.dump(self.ButtonLayout,json_data)

					with open("Setup.txt","r") as data:
						values = data.readlines()
						filename = pathname.split("\\")
						values[0] = 'CurrentLayout = "' + filename[len(filename)-1]+'"\n'
						self.CurrentLayout = filename[len(filename)-1]
					with open("Setup.txt","w") as data:
						data.writelines( values )

				except IOError:
					wx.LogError("Cannot save current data in file '%s'." % pathname)
		

	def Load(self):
		dirname = self.LayoutDir
		dlg = wx.FileDialog(self, "Load Layout File", dirname, "", "Layout files (json)|*.json", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

		if dlg.ShowModal() == wx.ID_CANCEL:
			return

		else:
			sel_dir = dlg.GetDirectory()
			if sel_dir != dirname:
				wx.MessageBox('Please choose a file in the correct directory', 'Error', wx.OK | wx.ICON_ERROR)
			
			else:
				pathname = dlg.GetPath()
				try:
					with open(pathname,"r") as json_data:
					   self.ButtonLayout = json.load(json_data)

					with open("Setup.txt","r") as data:
						values = data.readlines()
						filename = pathname.split("\\")
						values[0] = 'CurrentLayout = "' + filename[len(filename)-1]+'"\n'
						self.CurrentLayout = filename[len(filename)-1]

					with open("Setup.txt","w") as data:
						data.writelines( values )

				except IOError:
					wx.LogError("Cannot save current data in file '%s'." % pathname)

		with open(self.LayoutDir+"\\"+self.CurrentLayout) as json_data:
			self.ButtonLayout = json.load(json_data)

		for child in self.OptionPanel.GetChildren():
			if (child in self.StaticButtons) == False:
				child.Destroy()
		for i in range(0,5):
			for j in range(0,3):
				num = (i)+(j*5)
				Image = self.ButtonLayout["Button"+str(num+1)]["Image"]
				bmp = wx.Bitmap(self.ImageDir+Image, wx.BITMAP_TYPE_ANY)
				self.BitmapButtons[num].SetBitmapLabel(bmp)
				self.BitmapButtons[num].Refresh()

	def StartStopDeck(self,*args):
		try:
			print args
		except:
			args = False

		if (self.DeckState == True) | (args == True):
			si = subprocess.STARTUPINFO()
			si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.DeckThread.pid)], startupinfo=si)
			self.DeckState = False
			self.ToggleDeck.SetLabel("Start Deck")
			self.ToggleDeck.Refresh()

		elif self.DeckState == False:
			self.DeckThread = subprocess.Popen(os.getcwd()+"\ArduinoConnect.exe",shell=False)
			self.DeckState = True
			self.ToggleDeck.SetLabel("Stop Deck")
			self.ToggleDeck.Refresh()



	def Upload(self):
		if self.DeckState == True:
			self.StartStopDeck(False)
		if len(self.port) > 0:
			port = self.port
		else:
			ports = list(serial.tools.list_ports.comports())
			for p in ports:
				print str(p)
				if "Arduino Mega 2560" in str(p):
					port = str(p).split(" - ")[0]
					break

		command = [self.command]
		options = "--board arduino:avr:mega --port "+ port + " --upload " + os.getcwd()+"\ArduinoDeck\ArduinoDeck.ino"
		options = options.split()
		output = command + options
		NewButtonList = 'String files[] = {"'
		for i in range(0,len(self.ButtonLayout)):
			if i < len(self.ButtonLayout)-1:
				NewButtonList = NewButtonList + self.ButtonLayout["Button"+str(i+1)]["Image"].encode("utf-8")+'","'
			else:
				NewButtonList = NewButtonList + self.ButtonLayout["Button"+str(i+1)]["Image"].encode("utf-8")+'"};\n'
		with open(os.getcwd() + "\\ArduinoDeck\\ArduinoDeck.ino","r") as data:
			values = data.readlines()
			for i in range(0,len(values)):
				if "String files[]" in  values[i]:
					values[i] = NewButtonList

		with open(os.getcwd() + "\\ArduinoDeck\\ArduinoDeck.ino","w") as data:
			data.writelines( values )      
		self.UploadThread = subprocess.Popen(output,shell=False)

	def GetScenes(self):
		scenes = client.call(requests.GetSceneList())
		scene_list = []
		for i in scenes.getScenes():
			name = i['name']
			scene_list.append(name)
		return scene_list

	def GetSources(self,Scene):
		scenes = client.call(requests.GetSceneList())
		for i in scenes.getScenes():
			if i['name'] == Scene:
				sources = i['sources']
				source_list = [" "]
				for j in sources:
					name = j['name']
					source_list.append(name)
				return source_list


	###################################################################
	"""
	Functions for each specific action, including dropdown bars and buttons
	specifically for each one.
	"""

	#TWITCH

	def SubMode(self):
		SubText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Toggle Subscriber Only mode in Twitch chat.\nRequires valid Twitch chat settings in order to work; these can be found in the file Setup.py")
		SubText.SetForegroundColour("White")
	
	def EmoteMode(self):
		EmoteText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Toggle Emote Only mode in Twitch chat.\nRequires valid Twitch chat settings in order to work; these can be found in the file Setup.py")
		EmoteText.SetForegroundColour("White")
	
	def SlowMode(self):
		SlowText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Toggle Slow mode in Twitch chat.\nRequires valid Twitch chat settings in order to work; these can be found in the file Setup.py")
		SlowText.SetForegroundColour("White")
	
	def FollowerMode(self):
		FollowText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Toggle Follower Only mode in Twitch chat.\nRequires valid Twitch chat settings in order to work; these can be found in the file Setup.py")
		FollowText.SetForegroundColour("White")
	
	def Commercial(self):
		CommercialText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Launches an ad on the Twitch stream.\nRequires the streamer to be a Twitch Partner")
		CommercialText.SetForegroundColour("White")
	
	def CustomMessage(self):
		self.CustomText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Input custom message to be displayed in Twitch chat (Press enter to save message)")
		self.CustomText.SetForegroundColour("White")

		self.Message = wx.TextCtrl(self.OptionPanel, -1, "", pos=(8,28),size=(175, -1),style=wx.TE_PROCESS_ENTER)

		self.Message.Bind(wx.EVT_TEXT_ENTER, self.Finished)
		self.Message.Bind(wx.EVT_LEFT_DOWN, self.Clicked)
		self.Message.Bind(wx.EVT_TEXT,self.Clicked)

		self.Message.SetBackgroundColour("#272822")
		self.Message.SetForegroundColour("#c1c1bf")

		self.OptionPanelButtons = [self.Message]

	def Finished(self, event):
		NewMessage = event.GetEventObject().GetValue()
		self.ButtonLayout[self.ActiveButton.GetName()]["Action"]["Message"] = NewMessage
		self.Message.SetBackgroundColour("#272822")
		self.Refresh()

	def Clicked(self,event):
		self.Message.SetBackgroundColour("#575853")
		self.Refresh()
		event.Skip()
	
	#OBS
	def ToggleSource(self):
		self.SceneList = self.GetScenes()

		SceneText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Choose Scene:")
		SceneText.SetForegroundColour("White")

		SourceText = wx.StaticText(self.OptionPanel,-1,pos=(8,56),label="Choose Scene:")
		SourceText.SetForegroundColour("White")

		self.Scene = wx.Choice(self.OptionPanel, -1, pos=(8,28), choices=self.SceneList,name="Scene")
		self.Source = wx.Choice(self.OptionPanel, -1, pos=(8,76),choices=[],name="Source")

		self.OptionPanelButtons = [self.Scene,self.Source]

		for i in range(0,len(self.OptionPanelButtons)):
			self.OptionPanelButtons[i].SetBackgroundColour("#272822")
			self.OptionPanelButtons[i].SetForegroundColour("#c1c1bf")
		

	def ChooseScene(self):
		self.SceneList = self.GetScenes()

		SceneText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Choose Scene:")
		SceneText.SetForegroundColour("White")

		self.Scene = wx.Choice(self.OptionPanel, -1, pos=(8,28), choices=self.SceneList,name="Scene")

		print self.Scene
		print self.Scene.GetChildren()
		self.OptionPanelButtons = [self.Scene]

		for i in range(0,len(self.OptionPanelButtons)):
			self.OptionPanelButtons[i].SetBackgroundColour("#272822")
			self.OptionPanelButtons[i].SetForegroundColour("#c1c1bf")

	def Mic(self): 
		MicStateText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Microphone initial state:")
		MicStateText.SetForegroundColour("White")

		self.MicState = wx.Choice(self.OptionPanel,-1,choices=["Enabled","Disabled"],pos=(8,28),name="MicState")

		self.OptionPanelButtons = [self.MicState]

		for i in range(0,len(self.OptionPanelButtons)):
			self.OptionPanelButtons[i].SetBackgroundColour("#272822")
			self.OptionPanelButtons[i].SetForegroundColour("#c1c1bf")


	def Rec(self):
		RecStateText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Recording initial state:")
		RecStateText.SetForegroundColour("White")

		self.RecState = wx.Choice(self.OptionPanel,-1,choices=["Disabled","Enabled"],pos=(8,28),name="RecState")
		
		self.OptionPanelButtons = [self.RecState]

		for i in range(0,len(self.OptionPanelButtons)):
			self.OptionPanelButtons[i].SetBackgroundColour("#272822")
			self.OptionPanelButtons[i].SetForegroundColour("#c1c1bf")


	def Stream(self):
		StreamStateText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Stream initial state:")
		StreamStateText.SetForegroundColour("White")

		self.StreamState = wx.Choice(self.OptionPanel,-1,choices=["Disabled","Enabled"],pos=(8,28),name="StreamState")
		
		self.OptionPanelButtons = [self.StreamState]

		for i in range(0,len(self.OptionPanelButtons)):
			self.OptionPanelButtons[i].SetBackgroundColour("#272822")
			self.OptionPanelButtons[i].SetForegroundColour("#c1c1bf")

	#Media	
	def PreviousTrack(self):
		PrevText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Simulates a keypress of the Previous Track media key")
		PrevText.SetForegroundColour("White")

	def NextTrack(self):
		NextText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Simulates a keypress of the Next Track media key")
		NextText.SetForegroundColour("White")

	def PlayPause(self):
		PlayText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Simulates a keypress of the Play/Pause media key")
		PlayText.SetForegroundColour("White")

	def Mute(self):
		MuteText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Simulates a keypress of the Mute media key")
		MuteText.SetForegroundColour("White")

	def Stop(self):
		StopText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Simulates a keypress of the Stop media key")
		StopText.SetForegroundColour("White")

	def VolumeUp(self):
		VolUpText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Simulates a keypress of the Volume Up media key")
		VolUpText.SetForegroundColour("White")

	def VolumeDown(self):
		VolDownText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Simulates a keypress of the Volume Down media key")
		VolDownText.SetForegroundColour("White")



	def ChangeImage(self):
		ImageText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Choose an image:")
		ImageText.SetForegroundColour("White")

		self.Browse = wx.Button(self.OptionPanel,-1,pos=(8,28),label="Browse",name="PickImage",style=wx.BORDER_NONE)

		self.OptionPanelButtons = [self.Browse]

		for i in range(0,len(self.OptionPanelButtons)):
			self.OptionPanelButtons[i].SetBackgroundColour("#272822")
			self.OptionPanelButtons[i].SetForegroundColour("#c1c1bf")


		
	def Disable(self):
		SceneText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Choose Scene:")
		SceneText.SetForegroundColour("White")

		bmp = wx.Bitmap(self.ImageDir+"Disabled.bmp", wx.BITMAP_TYPE_ANY)
		self.ActiveButton.SetBitmapLabel(bmp)
		self.ActiveButton.Refresh()   
		self.ButtonLayout[self.ActiveButton.GetName()]["Image"] = "Disabled.bmp"
		self.ButtonLayout[self.ActiveButton.GetName()]["Action"] = None

	#Other Functions#
	def Hotkey(self):
		HotKeyText = wx.StaticText(self.OptionPanel,-1,pos=(8,8),label="Enter hotkey (Can use Shift and Ctrl):")
		HotKeyText.SetForegroundColour("White")

		self.HotKeyEnter = wx.TextCtrl(self.OptionPanel, -1, "", pos=(8,28),size=(175, -1))
		self.HotKeyEnter.SetInsertionPoint(0)

		self.hotkey = []

		self.HotKeyEnter.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
		self.HotKeyEnter.Bind(wx.EVT_KEY_UP, self.onKeyUp)

		self.OptionPanelButtons = [self.HotKeyEnter]

		for i in range(0,len(self.OptionPanelButtons)):
			  self.OptionPanelButtons[i].SetBackgroundColour("#272822")
			  self.OptionPanelButtons[i].SetForegroundColour("#c1c1bf")


	#Helper functions that other functions/actions require
	def PickImage(self):      
		dirname = os.getcwd()+"\ArduinoDeckIcons"
		dlg = wx.FileDialog(self, "Choose Image file", dirname, "", "Image files (bmp)|*.bmp|All files (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		my_file = ""

		if dlg.ShowModal() == wx.ID_CANCEL:
			pass
		else:
			sel_dir = dlg.GetDirectory()
			if sel_dir != dirname:
				wx.MessageBox('Please choose a file from the given directory', 'Error', wx.OK | wx.ICON_ERROR)
			else:
				try:
					my_file = dlg.GetFilename()

					try:
						bmp = wx.Bitmap(self.ImageDir+my_file, wx.BITMAP_TYPE_ANY)
						self.ActiveButton.SetBitmapLabel(bmp)
						self.ActiveButton.Refresh()   
						self.ButtonLayout[self.ActiveButton.GetName()]["Image"] = my_file

					except:
						self.ActiveButton.Refresh()   
						self.ButtonLayout[self.ActiveButton.GetName()]["Image"] = my_file
				except:
					None
						  
	def onKeyPress(self, event):
		keycode = event.GetKeyCode()
		if (keycode == wx.WXK_SHIFT) & (("shift" in self.hotkey) == False):
			self.hotkey.append("shift")
		if (keycode == wx.WXK_CONTROL) & (("ctrl" in self.hotkey) == False):
			self.hotkey.append("ctrl")
		if (32 < int(keycode) < 256):
			if ((chr(keycode).lower() in self.hotkey) == False):
				self.hotkey.append(chr(keycode).lower())

	def onKeyUp(self, event):
		if len(self.hotkey) > 0:
			self.HotKeyEnter.SetValue(' + '.join(self.hotkey))
			self.ButtonLayout[self.ActiveButton.GetName()]["Action"]["Hotkey"] = self.hotkey
		self.hotkey = []

########################################################################
class MainFrame(wx.Frame):

#----------------------------------------------------------------------
	  def __init__(self):

			wx.Frame.__init__(self, None, title="Arduino Deck",size=(870,750))
			self.panel = MainPanel(self)
			self.SetBackgroundColour("#272822")
			self.Bind(wx.EVT_CLOSE, self.OnClose)
			self.Show()

	  def OnClose(self,event):
			self.panel.OnClose()
			self.Destroy()

#----------------------------------------------------------------------
if __name__ == "__main__":
	  client = obsws("localhost", 4444, obspswd)
	  client_connected = False
	  try:
		client.connect()
		client_connected = True
	  except:
		None
	  app = wx.App(False)
	  frame = MainFrame()
	  app.MainLoop()
	  if client_connected == True:
		client.disconnect()