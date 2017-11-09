from obswebsocket import obsws, requests
import win32api
import serial
import datetime
import time
from urllib import urlopen
import pyautogui
import json
from Twitch import *



#TWITCH

def SubMode(client,Action):
	SendMessage("/subscribers","subs-only")
def EmoteMode(client,Action):
	SendMessage("/emoteonly","emote-only")
def FollowerMode(client,Action):
	SendMessage("/followers","followers-only")
def SlowMode(client,Action):
	SendMessage("/slow","slow")
def Commercial(client,Action):
	SendMessage("/commercial",None)
def CustomMessage(client,Action):
	SendMessage(Action["Message"],None)

#OBS

def ToggleSource(client,Action):
	Scene = Action["Scene"]
	Source = Action["Source"]
	scenes = client.call(requests.GetSceneList())
	for i in scenes.getScenes():
		if i['name'] == Scene:
			sources = i['sources']
			for j in sources:
				if j['name'] == Source:
					CurrentState = j['render']
					client.call(requests.SetSourceRender(Source,not CurrentState,Scene))

def ChooseScene(client,Action):
	Scene = Action["Scene"]
	client.call(requests.SetCurrentScene(Scene))

def Mic(client,Action):
	client.call(requests.ToggleMute("Mic/Aux"))

def Rec(client,Action):
	status = client.call(requests.GetStreamingStatus()).getRecording()
	client.call(requests.StartStopRecording(not status))

def Stream(client,Action):
	status = client.call(requests.GetStreamingStatus()).getRecording()
	client.call(requests.StartStopRecording(not status))

#MEDIA
def PreviousTrack(client,Action):
	KeyCode = 0xB1
	number = 0
	KeyPress(KeyCode,number)

def NextTrack(client,Action):
	KeyCode = 0xB0
	number = 1
	KeyPress(KeyCode,number)

def PlayPause(client,Action):
	KeyCode = 0xB3
	number = 2
	KeyPress(KeyCode,number)

def Mute(client,Action):
	KeyCode = 0xAD
	number = 3
	KeyPress(KeyCode,number)

def Stop(client,Action):
	KeyCode = 0xB2
	number = 4
	KeyPress(KeyCode,number)

def VolumeUp(client,Action):
	KeyCode = 0xAF
	number = 5
	KeyPress(KeyCode,number)

def VolumeDown(client,Action):
	KeyCode = 0xAE
	number = 6
	KeyPress(KeyCode,number)

def KeyPress(Key,number):
	hwcode = win32api.MapVirtualKey(Key,number)
	win32api.keybd_event(Key,hwcode)

#System Functions

def Hotkey(client,Action):
	pyautogui.hotkey(*Action["Hotkey"])