#!/usr/bin/env python

# standard packages
import sys
import socket
import string
import time
import re
import threading

# collected packages (pip install..)


# custom packages
import nicklist
import nickchan

def output(text):
  print("[%s] %s" % (time.strftime("%H:%M:%S"), text))


# all client variables
#### _VAR == client set variables
#### var == temporary variables
#### _VAR_ == global variables
output("& Loading variables ..")
_SERVER = "10.0.0.25"
_PORT = 6667
_BOTNICK = "damibawt"
_IDENT = "damibawt"
_REALNAME = "A robot!"
_TRIGGER = "!"

_BOTNAME = "boredBOT-py"
_BOTVER = "0.01"

# dont need to edit below this
_nicklist = nicklist.nicklist()
_chanlist = {}
_nickchan = nickchan.nickchan()
_server = {}
_bot = {}


output("& Loading functions ..");

###########################################################################################################
# for sending data to the network

# puts_data(<socket>, <data>) - puts data to the socket, converts it to bytes from string
def puts_data(data):
  irc.send(bytes("%s\r\n" % data, "utf-8"))
  debug(" <- %s" % data, -1)

# puts_join(<channel>) - joins the channel
def puts_join(chan):
  puts_data("JOIN %s" % chan)

# puts_part(<channel>, [<message>]) - parts the channel with message
def puts_part(chan, msg=''):
  puts_data("PART %s :%s" % (chan, msg))

def puts_quit(msg):
  puts_data("QUIT :%s" % msg)

def puts_msg(target, msg):
  puts_data("PRIVMSG %s :%s" % (target, msg))

def puts_notice(target, msg):
  puts_data("NOTICE %s :%s" % (target, msg))

def puts_kick(chan, nick, msg):
  puts_data("KICK %s %s :%s" % (chan, nick, msg))

def puts_topic(chan, msg):
  puts_data("TOPIC %s :%s" % (chan, msg))

def puts_pong(msg):
  puts_data("PONG :%s" % msg)

def puts_ctcp(target, msg):
  puts_data("PRIVMSG %s :%s%s%s" % (target, chr(1), msg, chr(1)))

def puts_ctcpr(target, msg):
  puts_data("NOTICE %s :%s%s%s" % (target, chr(1), msg, chr(1)))

def puts_who(msg):
  puts_data("WHO %s" % msg)

def puts_mode(target, mode):
  puts_data("MODE %s %s" % (target, mode))

def puts_invite(nick, chan):
  puts_data("INVITE %s %s" % (nick, chan))

def puts_nick(nick):
  puts_data("NICK %s" % nick)

def puts_user(ident, realname):
  puts_data("USER %s 0 * :%s" % (ident, realname))

#########################################################################################################
# these are functions for generic purposes
def lindex(text, num):
  # lindex("hello there bitch", 1) = "there"
  
  # split the text up
  text = text.split(" ")
  newtext = []
  
  # get rid of any spaces
  for word in text:
    if word:
      newtext.append(str(word))
      
  # return the output
  return newtext[num]

def lrange(text, first, last):
  # lrange("hello there bitch", 1, -1) = "there bitch"
  
  # split up the text
  text = text.split(" ")
  
  # this is the new array and the counter
  newtext = []
  i = 0
  
  # get rid of any spaces
  for word in text: # loop through all words
    if (i >= first) and ((i <= last) or (last == -1)):
      newtext.append(str(word))
    if word: # if it's an actual word and not ""
      i += 1
  
  # return the output
  return " ".join(newtext).strip()

# splits up nick!user@host to (nick, user, host); returns JUST nick if it's not a complete address
def split_fulladdress(address):
  if (re.match(".+!.+@.+", address)):
    return address.replace("!", " ").replace("@", " ").split(" ")
  else:
    return [address, "", ""]

def write(file, data):
  try:
    ofile = open(file, "a")
    ofile.write(data)
    ofile.close()
  except IOError:
    debug("write(%s); Unable to open file." % (file, data.strip("\r\n")))


def debug(text, level=0):
  # -1 = server data, write to server.debug.log
  # 0 = information
  # 1 = warning
  # 2 = error
  
  if (level == -1):
    write("server.debug.log", "%s %s\r\n" % (time.strftime("[%d/%m/%Y %H:%M:%S]"), text))
  else:
    level = ("Info" if (level == 0) else ("Warning" if (level == 1) else ("Error")))
    write("debug.log", "%s %s: %s\r\n" % (time.strftime("[%d/%m/%Y %H:%M:%S]"), level, text))

def addslashes(s):
  # thanks to http://www.php2python.com/wiki/function.addslashes/
    l = ["\\", '"', "'", "\0", ]
    for i in l:
        if i in s:
            s = s.replace(i, '\\'+i)
    return s
  

#########################################################################################################
# these functions will control the internal data; nicks, chans, etc
def mask(address, type):
  nick = address.split("!")[0]
  user = address.split("!")[1].split("@")[0]
  host = address.split("!")[1].split("@")[1]
  
  if (type == 1):
    # *!*damian@damian.id.au
    return "*!*%s@%s" % (user, host)
    
  elif (type == 2):
    # *!*@damian.id.au
    return "*!*@%s" % (host)
    
  elif (type == 3):
    # *!*damian@*.id.au
    return "*!*%s@*.%s" % (user, ".".join(host.split(".")[1:]))
    
  elif (type == 4):
    # *!*@*.id.au
    return "*!*@*.%s" % (".".join(host.split(".")[1:]))
    
  elif (type == 5):
    # damian!damian@damian.id.au
    return "%s!%s@%s" % (nick, user, host)
    
  elif (type == 6):
    # damian!*damian@damian.id.au
    return "%s!*%s@%s" % (nick, user, host)
    
  elif (type == 7):
    # damian!*@damian.id.au
    return "%s!*@%s" % (nick, host)
    
  elif (type == 8):
    # damian!*damian@*.id.au
    return "%s!*%s@*.%s" % (nick, user, ".".join(host.split(".")[1:]))
    
  elif (type == 9):
    # damian!*@*.id.au
    return "%s!*@*.%s" % (nick, ".".join(host.split(".")[1:]))
    
  elif (type == 10):
    # *!damian@damian.id.au
    return "*!%s@%s" % (user, host)


###########################################################################################################
# for getting data from the network

def gets_connected(server, botnick, network):
  # when the client connects to the network
  output("& Connected to %s [%s] as %s" % (server, network, botnick))
  _server['server'] = server
  _server['network'] = network
  _bot['nick'] = botnick
  
  puts_join("#nictitate")
  puts_msg("#nictitate", "hey bitches")
  
def gets_settings(settings):
  for setting in settings: # loop through all of the settings in the line
    setting = setting.split("=") # split it up so i can see setting/value
    if (len(setting) == 1): # if there's no value, it's true
      setting.append(True)
    
    setting = {'item': setting[0], 'value': setting[1]} # make a dict out of it

    if (setting['item'] == 'PREFIX'):
      mode = setting['value'][1:].split(")")
      modes = {}
      cnt = 0
      while (cnt < len(mode[0])):
        modes[mode[0][cnt]] = mode[1][cnt]
        cnt += 1
        
      _server['modes'] = modes
      
    if (setting['item'] == 'CHANMODES'):
      print("")

def gets_who(nick, user, host, name):
  output("~ Updated user detail for %s" % nick)
  _nicklist.add(nick, user, host, name)
  
  if (nick == _bot['nick']):
    _bot['user'] = user
    _bot['host'] = host
    _bot['name'] = name
  
def gets_names(chan, nicks):
  # after /names (or join chan)
  output("found these on %s: %s" % (chan, nicks))

def gets_ping(target):
  # when a ping/pong? happens
  puts_pong(target)

def gets_privmsg(nick, user, host, target, text):
  # on a privmsg
  
  if (re.match("#.+", target)): # a channel..
    if (re.match(chr(1) + "ACTION .+" + chr(1), text)): # if theres a chan/ACTION
      gets_chan_action(nick, user, host, target, lrange(text, 1, -1).rstrip(chr(1)))
      
    elif (re.match(chr(1) + ".+" + chr(1), text)): # if theres a chan/CTCP
      gets_ctcp(nick, user, host, text.strip(chr(1)))
      
    else: # any normal text
      gets_chan_msg(nick, user, host, target, text)
      
  else:
    if (re.match(chr(1) + "ACTION .+" + chr(1), text)): # if theres a user/ACTION
      gets_user_action(nick, user, host, lrange(text, 1, -1).rstrip(chr(1)))
      
    elif (re.match(chr(1) + ".+" + chr(1), text)): # if theres a user/CTCP
      gets_ctcp(nick, user, host, text.strip(chr(1)))
      
    else: # any normal text
      gets_user_msg(nick, user, host, text)

def gets_ctcp(nick, user, host, text):
  output("[%s %s] %s" % (nick, lindex(text, 0), lrange(text, 1, -1)))
  if (lindex(text, 0) == "VERSION"):
    puts_ctcpr(nick, "VERSION %s v%s - damian (Nov-2015)" % (_BOTNAME, _BOTVER))

def gets_chan_action(nick, user, host, chan, text):
  output("* %s:%s %s" % (nick, chan, text))

def gets_user_action(nick, user, host, text):
  output("* %s %s" % (nick, text))

def gets_chan_msg(nick, user, host, chan, text):
  output("<%s:%s> %s" % (nick, chan, text))
  if (text[:1] == _TRIGGER):
    if not (lindex(text, 0)[1:] in cmd):
      puts_notice(nick, "You specified an invalid command: %s" % lindex(text, 0)[1:])
    
    else:
      eval("user_%s(\"%s\", \"%s\", \"%s\", \"%s\")" % (lindex(text, 0)[1:], nick, user + "@" + host, chan, addslashes(lrange(text, 1, -1))))

def gets_user_msg(nick, user, host, text):
  output("<%s> %s" % (nick, text))

def gets_notice(nick, user, host, target, text):
  if (re.match("#.+", target)): # a channel..
    gets_chan_notice(nick, user, host, target, text)
    
  else:
    gets_user_notice(nick, user, host, text)

def gets_chan_notice(nick, user, host, chan, text):
  output("-%s:%s- %s" % (nick, chan, text))

def gets_user_notice(nick, user, host, text):
  output("-%s- %s" % (nick, text))
  
def gets_join(nick, user, host, chan):
  output("* %s (%s@%s) has joined %s" % (nick, user, host, chan))

  # update the nick/chan
  _nickchan.add(nick, chan)

  # update the internal address
  if (_nicklist.get(nick) is None):
    puts_who(nick)
  else:
    _nicklist.update(nick, 'user', user)
    _nicklist.update(nick, 'host', host)
  
  if (nick == _bot['nick']):
    puts_who(chan)
  

def gets_part(nick, user, host, chan, text):
  output("* %s (%s@%s) has parted %s [%s]" % (nick, user, host, chan, text))
  
def gets_kick(nick, user, host, chan, knick, text):
  output("* %s was kicked from %s by %s (%s@%s): %s" % (knick, chan, nick, user, host, text))
  
def gets_quit(nick, user, host, text):
  output("* %s (%s@%s) quit [%s]" % (nick, user, host, text))

def gets_error(text):
  output("!! ERROR: %s" % text)

###########################################################################################################
# commands, commands, commands! using a dictionary to make sure they exist
# the grunty code!
cmd = {
  'die': 300,
  'stats': 300,
  'op': 100,
  'deop': 100,
  'voice': 25,
  'devoice': 25,
  'nickinfo': 25,
  'tmp': 300
}

def user_tmp(nick, uhost, chan, text):
  puts_msg(chan, "OUTPUT: %s == %s" % (lindex(text, 0), mask(lindex(text, 0), int(lindex(text, 1)))))
  
def user_stats(nick, uhost, chan, text):
  puts_msg(chan, "nick: %s" % list(_nicklist.list().keys()))
  puts_msg(chan, "chan: %s" % _chanlist)
  puts_msg(chan, "nickchan: %s" % _nickchan)
  puts_msg(chan, "server: %s" % _server)
  puts_msg(chan, "bot: %s" % _bot)

def user_nickinfo(nick, uhost, chan, text):
  nickinfo = _nicklist.get(text)
  puts_msg(chan, "[%s!%s@%s]" % (nickinfo.nick(), nickinfo.user(), nickinfo.host()))
  
def user_die(nick, uhost, chan, text):
  puts_data("QUIT :%s said to quit! (%s)" % (nick, text))
  
def user_repeat(nick, uhost, chan, text):
  puts_msg(chan, "REPEATED: %s" % lrange(text, 1, -1))


# this is the read buffer, what will retrieve all of the data from the socket
def IRCBOT():
  global irc
  read = ""
  
  output("& Setting up socket ..")
  irc = socket.socket()
  
  output("& Connecting socket ..")
  irc.connect((_SERVER, _PORT))
  
  output("& Authenticating to server ..")
  puts_nick(_BOTNICK)
  puts_user(_IDENT, _REALNAME)
  
  output("& Starting data loop ..")
  while 1:
    # read the receive buffer (1kb at a time)
    read = read + irc.recv(1024).decode("utf-8")
    
    # check if socket still exists..
    if (len(read) == 0):
      break
  
    # split the read buffer into lines
    lines = str.split(read, "\n")
    
    # set the receive buffer to any left over data before next \n (and clear it from lines)
    read = lines.pop()
    
    for line in lines:
      # output to screen
      debug(" -> %s" % line, -1)
        
      if (lindex(line, 0) == "PING"):
        gets_ping(lindex(line, 1)[1:])
        
      if (lindex(line, 1) == "001"):
        # :Welcome to the Internet Relay Network <nick>!<user>@<host>
        gets_connected(lindex(line, 0)[1:], lindex(line, 2), lindex(line, 6))
          
      if (lindex(line, 1) == "005"):
        gets_settings(lrange(line, 3, -1).split(" ")[:-5])
        
      if (lindex(line, 1) == "352"):
        # <channel> <user> <host> <server> <nick> <H|G>[*][@|+] :<hopcount> <real_name>
        gets_who(lindex(line, 7), lindex(line, 4), lindex(line, 5), lrange(line, 10, -1))

      if (lindex(line, 1) == "353"):
        # ( '=' / '*' / '@' ) <channel> ' ' : [ '@' / '+' ] <nick> *( ' ' [ '@' / '+' ] <nick> )
        gets_names(lindex(line, 4), lrange(line, 5, -1)[1:].split(" "))
        
      if (lindex(line, 1) == "433"):
        gets_nick_exists(lindex(line, 3))
        
      if (lindex(line, 1) == "PRIVMSG"):
        (nick, user, host) = split_fulladdress(lindex(line, 0)[1:])
        gets_privmsg(nick, user, host, lindex(line, 2), lrange(line, 3, -1)[1:])
        
      if (lindex(line, 1) == "NOTICE"):
        (nick, user, host) = split_fulladdress(lindex(line, 0)[1:])
        gets_notice(nick, user, host, lindex(line, 2), lrange(line, 3, -1)[1:])
      
      if (lindex(line, 1) == "JOIN"):
        (nick, user, host) = split_fulladdress(lindex(line, 0)[1:])
        gets_join(nick, user, host, lindex(line, 2).lstrip(":"))
        
      if (lindex(line, 1) == "PART"):
        (nick, user, host) = split_fulladdress(lindex(line, 0)[1:])
        gets_part(nick, user, host, lindex(line, 2), lrange(line, 3, -1)[1:])
        
      if (lindex(line, 1) == "QUIT"):
        (nick, user, host) = split_fulladdress(lindex(line, 0)[1:])
        gets_quit(nick, user, host, lrange(line, 2, -1)[1:])
        
      if (lindex(line, 1) == "KICK"):
        (nick, user, host) = split_fulladdress(lindex(line, 0)[1:])
        gets_kick(nick, user, host, lindex(line, 2), lindex(line, 3), lrange(line, 4, -1)[1:])
        
      if (lindex(line, 0) == "ERROR"):
        gets_error(lrange(line, 1, -1)[1:])

IRCThread = threading.Thread(target = IRCBOT, args = ())
IRCThread.start()


KILL = False
while not KILL:
  text = input()
  if (text[:1] == "/"):
    if (lindex(text, 0) == "/quit"):
      puts_data("QUIT :Console terminated by user.")
      time.sleep(3)
      KILL = True
      
    elif (lindex(text, 0) == "/msg"):
      # /msg target message
      output("-> *%s* %s" % (lindex(text, 1), lrange(text, 2, -1)))
      puts_msg(lindex(text, 1), lrange(text, 2, -1))
    
    elif (lindex(text, 0) == "/reload"):
      reload(boredbot)
    else:
      print("ERROR: I don't have that command yet.")

  else:
    puts_data(text)
    print("> Command executed: %s" % text)





output("")
print("Waiting 10secs before close: ", end="")
for i in range(10, 0, -1):
  print("%s.. " % i, end="")
  sys.stdout.flush()
  time.sleep(1)






