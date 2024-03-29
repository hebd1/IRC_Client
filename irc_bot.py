#!/usr/bin/python3

import socket

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net" 
channel = "##bot-tester"
botnick = "PyBuddy"
adminname = "hebd1"
exitcode = "bye " + botnick.lower()


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
        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!',1) [0] [1:]
            message = ircmsg.split('PRIVMSG',1) [1].split(':',1) [1] 
            if len(name) < 17:
                if message.lower().find('hi ' + botnick.lower()) != -1:
                    sendmsg("Hello " + name + "!") 
                if message[:5].find('.tell') != -1:
                    target = message.split(' ', 1) [1]
                    if target.find(' ') != -1:
                        message = target.split(' ',1) [1]
                        target = target.split(' ') [0] 
                    else:
                        target = name
                        message = "Could not parse. The message should be formatted as '.tell [target] [message]'"
                    sendmsg(message, target) 
                if name.lower() == adminname.lower() and message.lower().rstrip() == exitcode:
                    sendmsg("oh..okay then :'(") 
                    ircsock.send(bytes("QUIT \n", "UTF-8"))
                    return
        else:
            if ircmsg.find("PING :") != -1:
                ping()

main()



