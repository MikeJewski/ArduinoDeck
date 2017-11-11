import re
import socket
import time


def SendMessage(msg,check):

	ChannelName = ""
	TwitchChatKey = ""
	with open("Setup.txt","r") as data:
                  values = data.readlines()
                  for i in range(0,len(values)):
                        exec(values[i] )
                        
	HOST = "irc.chat.twitch.tv"
	PORT = 6667                        
	NICK = ChannelName
	PASS = "oauth:" + TwitchChatKey
	CHAN = "#" + ChannelName

	public = socket.create_connection((HOST, PORT))
	public.send("PASS {}\r\n".format(PASS).encode("utf-8"))
	public.send("NICK {}\r\n".format(NICK).encode("utf-8"))
	public.send("CAP REQ :twitch.tv/membership\r\n".encode("utf-8"))
	public.send("CAP REQ :twitch.tv/commands\r\n".encode("utf-8"))
	public.send("CAP REQ :twitch.tv/tags\r\n".encode("utf-8"))
	public.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

	end = True 

	if (check != None):
		while end:
			message = public.recv(1024).decode("utf-8")

			if (("ROOMSTATE" in message) == True):
				roomstates = message.split(" :tmi.twitch.tv")[1].split(";")
				print roomstates
				for i in range(0,len(roomstates)):
					if(check in roomstates[i]):
						print msg
						if (int(roomstates[i].split("=")[1]) == 0)|(int(roomstates[i].split("=")[1]) == -1):
							public.send("PRIVMSG " + CHAN+ " : %s \r\n"%(msg).encode("utf-8"))
							end = False
						else:
							public.send("PRIVMSG " + CHAN+ " : %s \r\n"%(msg + "off").encode("utf-8"))
							end = False
	else:
		public.send("PRIVMSG " + CHAN+ " : %s \r\n"%(msg).encode("utf-8"))
		return None
