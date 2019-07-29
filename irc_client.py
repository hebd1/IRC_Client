#!/usr/bin/python3

import socket

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net" 
channel = "##bot-tester"
botnick = "hebd1"
adminname = "hebd1"


ircsock.connect((server, 6667))
ircsock.send(bytes("USER " + botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8"))
ircsock.send(bytes("NICK " + botnick + "\n", "UTF-8"))

def joinchan(chan):
    ircsock.send(bytes("JOIN " + chan + "\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8") 
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg) 

def ping():
        ircsock.send(bytes("PONG :pingis\n", "UTF-8")) 


def sendmsg(msg, target=channel):
    ircsock.send(bytes("PRIVMSG "+ target + " :" + msg + "\n", "UTF-8")) 

def main():
    joinchan(channel)
    while 1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r') 
        print(ircmsg)
        if ircmsg.find("PING :") != -1:
            ping()
        else:
            outmsg = input(botnick + ": ") 
            sendmsg(outmsg)



main()



