from obswebsocket import obsws, requests
import win32api
import serial
import datetime
import time
import json
from Actions import *
import os
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for p in ports:
	if "Arduino Mega 2560" in str(p):
		port = str(p).split(" - ")[0]
		break
States = []
LayoutDir = os.getcwd()+"\\Layouts"

with open("Setup.txt","r") as data:
	values = data.readlines()
	for i in range(0,len(values)):
		exec(values[i])

with open(LayoutDir+"\\"+CurrentLayout,"r") as json_data:
	States = json.load(json_data)
try:
	client = obsws("localhost", 4444, obspswd)
	client.connect()
	client.call(requests.SetMute("Mic/Aux",False))
except:
	None
ser = serial.Serial(port,9600,timeout=0)
BaseTime = datetime.datetime.now().strftime('%M')
curr_time = datetime.datetime.now().strftime('%H:%M')
ser.write(ser.write(str(curr_time)+','+str('N/A')+','+str('N/A')))
try:
	while True:
		StreamDeck = ser.readline().rstrip()
		try:
			if(StreamDeck.isdigit()):
				Action = States["Button"+StreamDeck]["Action"]
				exec(Action["Name"]+"(client,Action)")
		except Exception as e:
			print(e)

		now = datetime.datetime.now().strftime('%M')

		if ((int(now) - int(BaseTime) > 0) & (int(BaseTime) <59))|(int(now)-int(BaseTime) == -59):
			BaseTime = now
			#Time to print to the display
			curr_time = datetime.datetime.now().strftime('%H:%M')

			site = "https://api.twitch.tv/kraken/streams?channel=" + ChannelName+ "&oauth_token=" + TwitchChatKey
			info = json.loads(urlopen(site).read())

			#Number of viewers to print
			#Hotfix to deal with people who don't want to connect to Twitch
			try:
				if info["_total"] != 0: 
					viewers = info["streams"][0]["viewers"]
					a = info['streams'][0]['created_at']
					b = datetime.datetime.now()+datetime.timedelta(hours=4)
					c = datetime.datetime.strptime(a, "%Y-%m-%dT%H:%M:%SZ")
					d = b-c
					e = (datetime.datetime.min+d).time().strftime('%H:%M')
				else:
					viewers = "N/A"
					e = "N/A"
			except:
				viewers = "N/A"
				e = "N/A"
				
			ser.write(str(curr_time)+','+str(viewers)+','+str(e))
		time.sleep(0.2)

except:
	ser.close()
	try:
		client.disconnect()
	except:
		None
