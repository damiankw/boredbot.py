#!/usr/bin/env python

# standard packages
import sys
import socket
import string
import time
import re
import threading
import traceback
import logging
import importlib

# set up my import folders
sys.path.insert(0, 'src')

# custom packages
from general import *
from nicklist import *
from nickchan import *
from chanlist import *

class boredbot():
  # default variables for use later
  SERVER = {} # server information that should be stored
  BOT = {} # bot information that should be stored
  
  SYSTEM = { # system variables - these don't change
    'name': 'boredBOT-py',
    'version': '0.02',
    'phrase': 'classy',    # classy .. the first version where i truely start using classes
    'creator': 'damian <damian@damian.id.au>',
    'date': '30/11/2015'
  }

  def __init__(self, nick=None, ident=None, name=None):
    output("", show_time = False)
    output("%s v%s \"%s\" 2015 by %s" % (self.SYSTEM['name'], self.SYSTEM['version'], self.SYSTEM['phrase'], self.SYSTEM['creator']), show_time = False)

    if (type(nick) is dict): # check if we were passed a settings variable (can hold more settings)
      self.CONFIG = nick

    else: # go by the variables given
      # set up the CONFIG from variables
      self.CONFIG = {
        'nick': nick,                  # given from init()
        'ident': ident,                # given from init()
        'name': name,                  # given from init()
        'server': 'irc.nerdhacks.net', # default
        'port': 6667,                  # default
        'cmd': '!'                     # default
      }
    
    output("& Setting up socket ..")
    self.IRCSOCK = socket.socket()
    
    # set up the nicklist
    self.NICKLIST = nicklist()
    
    # set up the chanlist
    self.CHANLIST = chanlist()
    
    # set up the nickchan
    self.NICKCHAN = nickchan()
  
  def connect(self, server=None, port=None):
    IRCBOT = threading.Thread(target = self.start, args = ())
    IRCBOT.start()

  def start(self, server=None, port=None): # *.connect() // *.connect('server', 'port')
    read = ""
    
    output("& Connecting socket ..")
    self.IRCSOCK.connect((self.CONFIG['server'], self.CONFIG['port']))
    
    output("& Authenticating to server ..")
    self.puts_nick(self.CONFIG['nick'])
    self.puts_user(self.CONFIG['ident'], self.CONFIG['name'])
    
    output("& Starting data loop ..")
    while 1:
      # read the receive buffer (1kb at a time)
      read = read + self.IRCSOCK.recv(1024).decode("utf-8")
      
      # check if socket still exists..
      if (len(read) == 0):
        break
    
      # split the read buffer into lines
      lines = str.split(read, "\n")
      
      # set the receive buffer to any left over data before next \n (and clear it from lines)
      read = lines.pop()
      
      for line in lines:
        # clean up the line (remove \r)
        line = line.strip("\r")
        
        # output to screen
        debug(" -> %s" % line, -1)
          
        if (lindex(line, 0) == "PING"):
          self.gets_ping(lindex(line, 1)[1:])
          
        if (lindex(line, 0) == "ERROR"):
          # ERROR :Closing Link: damibawt[10.0.0.159] (Quit: damian said to quit! ())
          self.gets_error(lrange(line, 1, -1)[1:])
          
        if (lindex(line, 1) == "001"):
          # :asuna.nerdhacks.net 001 damibawt :Welcome to the nerdhacks IRC Network damibawt!damibawt@CPE-61-9-139-58.static.vic.bigpond.net.au
          self.gets_connected(lindex(line, 0)[1:], lindex(line, 2), lindex(line, 6))
            
        if (lindex(line, 1) == "005"):
          # :asuna.nerdhacks.net 005 damibawt CMDS=KNOCK,MAP,DCCALLOW,USERIP,STARTTLS UHNAMES NAMESX SAFELIST HCN MAXCHANNELS=30 CHANLIMIT=#:30 MAXLIST=b:60,e:60,I:60 NICKLEN=30 CHANNELLEN=32 TOPICLEN=307 KICKLEN=307 AWAYLEN=307 :are supported by this server
          # :asuna.nerdhacks.net 005 damibawt MAXTARGETS=20 WALLCHOPS WATCH=128 WATCHOPTS=A SILENCE=15 MODES=12 CHANTYPES=# PREFIX=(ohv)@%+ CHANMODES=beIqa,kfL,lj,psmntirRcOAQKVCuzNSMTGZ NETWORK=nerdhacks CASEMAPPING=ascii EXTBAN=~,qjncrRa ELIST=MNUCT :are supported by this server
          # :asuna.nerdhacks.net 005 damibawt STATUSMSG=@%+ EXCEPTS INVEX :are supported by this server
          self.gets_005(lrange(line, 3, -1).split(" ")[:-5])
          
        if (lindex(line, 1) == "324"):
          # :nictitate.nerdhacks.net 324 damibawt #nictitate +nt 
          self.gets_324(lindex(line, 3), lindex(line, 4))
          
        if (lindex(line, 1) == "329"):
          # :nictitate.nerdhacks.net 329 damibawt #nictitate 1442055000
          self.gets_329(lindex(line, 3), lindex(line, 4))
          
        if (lindex(line, 1) == "332"):
          # :nictitate.nerdhacks.net 332 damibawt #nictitate :the official home of nictitate.*, asit.* and stable.*
          self.gets_332(lindex(line, 3), lrange(line, 4, -1)[1:])
          
        if (lindex(line, 1) == "333"):
          # :asuna.nerdhacks.net 333 damibawt #nictitate damian 1447321715
          self.gets_333(lindex(line, 3), lindex(line, 4), lindex(line, 5))
          
        if (lindex(line, 1) == "352"):
          # <channel> <user> <host> <server> <nick> <H|G>[*][@|+] :<hopcount> <real_name>
          self.gets_352(lindex(line, 7), lindex(line, 4), lindex(line, 5), lrange(line, 10, -1))
  
        if (lindex(line, 1) == "353"):
          # ( '=' / '*' / '@' ) <channel> ' ' : [ '@' / '+' ] <nick> *( ' ' [ '@' / '+' ] <nick> )
          self.gets_353(lindex(line, 4), lrange(line, 5, -1)[1:].split(" "))
          
        if (lindex(line, 1) == "433"):
          # :nictitate.nerdhacks.net 353 damibawt = #nictitate :damibawt!damibawt@68E73386.B36784A9.393A910F.IP dmaina!damian@68E73386.B36784A9.393A910F.IP stevo!stevo@9E120BD5.CB4CC13.682EC28E.IP damiwork!damian@nerd-4661C0DE.austsup.local %+damian!damian@damian.id.au Stable!stable@E4AE59B3.B36784A9.393A910F.IP saint!saint@81F4F82.FD1E259C.4F953C86.IP 
          self.gets_433(lindex(line, 3))
          
        if (lindex(line, 1) == "PRIVMSG"):
          # :damian!damian@68E73386.B36784A9.393A910F.IP PRIVMSG #nictitate :channel message
          # :damian!damian@68E73386.B36784A9.393A910F.IP PRIVMSG damibawt :private message
          (nick, user, host) = split_fulladdress(lindex(line, 0)[1:])
          self.gets_privmsg(nick, user, host, lindex(line, 2), lrange(line, 3, -1)[1:])
          
        if (lindex(line, 1) == "NOTICE"):
          # :asuna.nerdhacks.net NOTICE AUTH :*** Looking up your hostname...
          # :damian!damian@68E73386.B36784A9.393A910F.IP NOTICE #nictitate :channel notice
          # :damian!damian@68E73386.B36784A9.393A910F.IP NOTICE damibawt :private notice
          (nick, user, host) = split_fulladdress(lindex(line, 0)[1:])
          self.gets_notice(nick, user, host, lindex(line, 2), lrange(line, 3, -1)[1:])
        
        if (lindex(line, 1) == "JOIN"):
          # :damibawt!damibawt@68E73386.B36784A9.393A910F.IP JOIN :#nictitate
          (nick, user, host) = split_fulladdress(lindex(line, 0)[1:])
          self.gets_join(nick, user, host, lindex(line, 2).lstrip(":"))
          
        if (lindex(line, 1) == "PART"):
          # :damibawt!damibawt@68E73386.B36784A9.393A910F.IP PART #nictitate
          (nick, user, host) = split_fulladdress(lindex(line, 0)[1:])
          self.gets_part(nick, user, host, lindex(line, 2), lrange(line, 3, -1)[1:])
          
        if (lindex(line, 1) == "QUIT"):
          (nick, user, host) = split_fulladdress(lindex(line, 0)[1:])
          self.gets_quit(nick, user, host, lrange(line, 2, -1)[1:])
          
        if (lindex(line, 1) == "KICK"):
          # :ChanOP!service@nerdhacks.net KICK #nictitate damibawt :[damian] User Kick requested
          (nick, user, host) = split_fulladdress(lindex(line, 0)[1:])
          self.gets_kick(nick, user, host, lindex(line, 2), lindex(line, 3), lrange(line, 4, -1)[1:])


  ###########################################################################################################
  # for sending data to the network
  
  # puts_data(<socket>, <data>) - puts data to the socket, converts it to bytes from string
  def puts_data(self, data):
    self.IRCSOCK.send(bytes("%s\r\n" % data, "utf-8"))
    debug(" <- %s" % data, -1)
 
  # puts_join(<channel>) - joins the channel
  def puts_join(self, chan):
    self.puts_data("JOIN %s" % chan)

  # puts_part(<channel>, [<message>]) - parts the channel with message
  def puts_part(self, chan, msg=''):
    self.puts_data("PART %s :%s" % (chan, msg))
  
  def puts_quit(self, msg):
    self.puts_data("QUIT :%s" % msg)
  
  def puts_msg(self, target, msg):
    for line in str(msg).split("\n"):
      while (line != ""):
        self.puts_data("PRIVMSG %s :%s" % (target, line[0:430]))
        line = line[430:]
        
  def puts_notice(self, target, msg):
    for line in msg.split("\n"):
      self.puts_data("NOTICE %s :%s" % (target, line))
  
  def puts_kick(self, chan, nick, msg):
    self.puts_data("KICK %s %s :%s" % (chan, nick, msg))
  
  def puts_topic(self, chan, msg):
    self.puts_data("TOPIC %s :%s" % (chan, msg))
  
  def puts_pong(self, msg):
    self.puts_data("PONG :%s" % msg)
  
  def puts_ctcp(self, target, msg):
    self.puts_data("PRIVMSG %s :%s%s%s" % (target, chr(1), msg, chr(1)))
  
  def puts_ctcpr(self, target, msg):
    self.puts_data("NOTICE %s :%s%s%s" % (target, chr(1), msg, chr(1)))
  
  def puts_who(self, msg):
    self.puts_data("WHO %s" % msg)
  
  def puts_mode(self, target, mode=""):
    self.puts_data("MODE %s %s" % (target, mode))
  
  def puts_invite(self, nick, chan):
    self.puts_data("INVITE %s %s" % (nick, chan))
  
  def puts_nick(self, nick):
    self.puts_data("NICK %s" % nick)
  
  def puts_user(self, ident, realname):
    self.puts_data("USER %s 0 * :%s" % (ident, realname))

  #########################################################################################################
  # these are functions for generic purposes
  
  
  #########################################################################################################
  # these functions will control the internal data; nicks, chans, etc
  # splits up nick!user@host to (nick, user, host); returns JUST nick if it's not a complete address
  
  ###########################################################################################################
  # for getting data from the network
  
  def gets_connected(self, server, botnick, network):
    # when the client connects to the network
    output("& Connected to %s [%s] as %s" % (server, network, botnick))
    self.SERVER['server'] = server
    self.SERVER['network'] = network
    self.BOT['nick'] = botnick
    
    # tell the server what the bot can understand
    self.puts_data("PROTOCTL NAMESX")
    self.puts_data("PROTOCTL UHNAMES")
    
    # general things to do on connect
    self.puts_join("#nerdhacks")
    
  def gets_005(self, settings):
    for setting in settings: # loop through all of the settings in the line
      setting = setting.split("=") # split it up so i can see setting/value
      if (len(setting) == 1): # if there's no value, it's true
        setting.append(True)
      
      setting = {'item': setting[0], 'value': setting[1]} # make a dict out of it
  
      if (setting['item'] == "PREFIX"):
        mode = setting['value'][1:].split(")")
        modes = {}
        cnt = 0
        while (cnt < len(mode[0])):
          modes[mode[0][cnt]] = mode[1][cnt]
          cnt += 1
          
        self.SERVER['modes'] = modes
        
      if (setting['item'] == "CHANMODES"):
        print("")
  
  def gets_352(self, nick, user, host, name):
    output("~ Updated user detail for %s" % nick)
    #self.NICKLIST.add(nick, user, host)
    
    
  def gets_353(self, chan, nicks):
    for item in nicks: # loop through the nicknames
      mode = [] # array to store modes
          
      if ("!" in item): # if we have full nick!user@host, split the host
        nick = item.split("!")[0]
        user = item.split("!")[1].split("@")[0]
        host = item.split("!")[1].split("@")[1]
      else:
        nick = item
        
      for char in nick:
        if (is_mode(char, self.SERVER['modes'])):
          mode.append(char2mode(char, self.SERVER['modes']))
          nick = nick[1:]
  
      self.NICKLIST.add(nick, user, host)
      self.NICKCHAN.add(nick, chan)
      self.NICKCHAN.set_mode(nick, chan, mode)
      
      if (nick == self.BOT['nick']):
        self.BOT['user'] = user
        self.BOT['host'] = host
  
  def gets_332(self, chan, topic):
    output("*** Topic in %s: %s" % (chan, topic))
    self.CHANLIST.update(chan, 'topic', topic)
  
  def gets_333(self, chan, nick, date):
    output("*** Set by: %s on %s" % (nick, time.strftime("%a, %d %b %Y %H:%M:%S")))
    self.CHANLIST.update(chan, 'topic_by', nick)
    self.CHANLIST.update(chan, 'topic_date', date)
    
  def gets_324(self, chan, mode):
    output("*** Mode on %s: %s" % (chan, mode))
    
  def gets_329(self, chan, date):
    output("*** Created: %s" % time.strftime("%a, %d %b %Y %H:%M:%S"))
    
  def gets_ping(self, target):
    # when a ping/pong? happens
    self.puts_pong(target)
  
  def gets_privmsg(self, nick, user, host, target, text):
    # on a privmsg
    
    if (re.match("#.+", target)): # a channel..
      if (re.match(chr(1) + "ACTION .+" + chr(1), text)): # if theres a chan/ACTION
        self.gets_chan_action(nick, user, host, target, lrange(text, 1, -1).rstrip(chr(1)))
        
      elif (re.match(chr(1) + ".+" + chr(1), text)): # if theres a chan/CTCP
        self.gets_ctcp(nick, user, host, text.strip(chr(1)))
        
      else: # any normal text
        self.gets_chan_msg(nick, user, host, target, text)
        
    else:
      if (re.match(chr(1) + "ACTION .+" + chr(1), text)): # if theres a user/ACTION
        self.gets_user_action(nick, user, host, lrange(text, 1, -1).rstrip(chr(1)))
        
      elif (re.match(chr(1) + ".+" + chr(1), text)): # if theres a user/CTCP
        self.gets_ctcp(nick, user, host, text.strip(chr(1)))
        
      else: # any normal text
        self.gets_user_msg(nick, user, host, text)
  
  def gets_ctcp(self, nick, user, host, text):
    output("[%s %s] %s" % (nick, lindex(text, 0), lrange(text, 1, -1)))
    if (lindex(text, 0) == "VERSION"):
      self.puts_ctcpr(nick, "VERSION %s v%s \"%s%s%s\" - damian (%s)" % (self.SYSTEM['name'], self.SYSTEM['version'], chr(29), self.SYSTEM['phrase'], chr(29), self.SYSTEM['date']))
  
  def gets_chan_action(self, nick, user, host, chan, text):
    output("* %s:%s %s" % (nick, chan, text))
  
  def gets_user_action(self, nick, user, host, text):
    output("* %s %s" % (nick, text))
  
  def gets_chan_msg(self, nick, user, host, chan, text):
    output("<%s:%s> %s" % (nick, chan, text))
    if (text[:1] == self.CONFIG['cmd']):
      try:
        # we throw these to a timer ..... jussssttttttt in case they take a while
        cmd = threading.Thread(target = eval("self.user_%s" % lindex(text, 0)[1:]), args = (nick, user + "@" + host, chan, addslashes(lrange(text, 1, -1))))
        cmd.start()
        output("!%s! (%s!%s@%s) %s - %s" % (lindex(text, 0)[1:].upper(), nick, user, host, chan, lrange(text, 1, -1)))
      except AttributeError:
        return
  
  def gets_user_msg(self, nick, user, host, text):
    output("<%s> %s" % (nick, text))
  
  def gets_notice(self, nick, user, host, target, text):
    if (re.match("#.+", target)): # a channel..
      self.gets_chan_notice(nick, user, host, target, text)
      
    else:
      self.gets_user_notice(nick, user, host, text)
  
  def gets_chan_notice(self, nick, user, host, chan, text):
    output("-%s:%s- %s" % (nick, chan, text))
  
  def gets_user_notice(self, nick, user, host, text):
    output("-%s- %s" % (nick, text))
    
  def gets_join(self, nick, user, host, chan):
    output("*** %s (%s@%s) has joined %s" % (nick, user, host, chan))
    # update the nick/chan
    self.NICKCHAN.add(nick, chan)
    self.NICKLIST.add(nick, user, host)
    
    if (nick == self.BOT['nick']):
      self.bot_join(chan)
  

  def bot_join(self, chan):
    self.CHANLIST.add(chan)
    self.puts_mode(chan)

  def gets_part(self, nick, user, host, chan, text):
    output("*** %s (%s@%s) has parted %s [%s]" % (nick, user, host, chan, text))
    self.NICKCHAN.remove(nick, chan)
    
    # check if this is the last channel the user is on - delete user data
    if (self.NICKCHAN.get_chan(nick) == None):
      self.NICKLIST.remove(nick)
    
    # check if it's the bot
    if (nick == self.BOT['nick']):
      self.bot_part(chan)
    
  def bot_part(self, chan):
    # if it's the bot, delete channel and user data from the channel
    for user in self.NICKCHAN.get_nick(chan):
      self.NICKCHAN.remove(user, chan)
      if (self.NICKCHAN.get_chan(user) == None):
        self.NICKLIST.remove(user)
      
    self.CHANLIST.remove(chan)
    
  def gets_kick(self, nick, user, host, chan, knick, text):
    output("*** %s was kicked from %s by %s (%s@%s): %s" % (knick, chan, nick, user, host, text))
    self.NICKCHAN.remove(knick, chan)
    
    # check if this is the last channel the user is on - delete user data
    if (self.NICKCHAN.get_chan(knick) == None):
      self.NICKLIST.remove(knick)
    
    if (knick == self.BOT['nick']):
      self.bot_part(chan)
      self.puts_join(chan)
    
  def gets_quit(self, nick, user, host, text):
    output("*** %s (%s@%s) quit [%s]" % (nick, user, host, text))
    for chan in self.NICKCHAN.get_chan(nick):
      self.NICKCHAN.remove(nick, chan)
    
    # delete the nick from the list
    self.NICKLIST.remove(nick)
    
    if (nick == self.BOT['nick']):
      self.bot_quit(chan)
  
  def bot_quit(self, chan):
    # need to delete everything here
    output("bot quit")
  
  def gets_error(self, text):
    output("!! ERROR: %s" % text)
  
  ###########################################################################################################
  # commands, commands, commands! using a dictionary to make sure they exist
  # the grunty code!
  def user_listchan(self, nick, uhost, chan, text):
    self.puts_msg(chan, "%s is on channels: %s" % (lindex(text, 0), self.NICKCHAN.get_chan(lindex(text, 0))))
    
  def user_listnick(self, nick, uhost, chan, text):
    self.puts_msg(chan, "%s has these users: %s" % (lindex(text, 0), self.NICKCHAN.get_nick(lindex(text, 0))))
    
  def user_eval(self, nick, uhost, chan, text):
    if (text == ""):
      self.puts_notice(nick, "try putting some eval in, ass.")
      return
    try:
      self.puts_msg(chan, eval("%s" % removeslashes(text)))
    except Exception as ex:
      #self.puts_msg(chan, "> %s" % removeslashes(text)) # just in case error doesnt make sense
      self.puts_msg(chan, "Py error: %s" % str(ex))
      
    self.puts_msg(chan, "End.")
    
  def user_stats(self, nick, uhost, chan, text):
    self.puts_msg(chan, "nick: %s" % self.NICKLIST.list())
    self.puts_msg(chan, "chan: %s" % self.CHANLIST.list())
    self.puts_msg(chan, "nickchan: %s" % self.NICKCHAN.list())
    self.puts_msg(chan, "server: %s" % self.SERVER)
    self.puts_msg(chan, "bot: %s" % self.BOT)
    self.puts_msg(chan, "-------------------------------------------------------------------")
    
  def user_nickinfo(self, nick, uhost, chan, text):
    nickinfo = self.NICKLIST.get(text)
    self.puts_msg(chan, "[%s!%s@%s]" % (nickinfo.nick(), nickinfo.user(), nickinfo.host()))
    
  def user_die(self, nick, uhost, chan, text):
    self.puts_data("QUIT :%s said to quit! (%s)" % (nick, text))
    
  def user_repeat(self, nick, uhost, chan, text):
    self.puts_msg(chan, "REPEATED: %s" % lrange(text, 1, -1))
  
  
  # this is the read buffer, what will retrieve all of the data from the socket

  def catch(self):
    KILL = False
    while not KILL:
      text = input()
      if (text[:1] == "/"):
        if (lindex(text, 0) == "/quit"):
          self.puts_data("QUIT :Console terminated by user.")
          time.sleep(1)
          KILL = True
          
        elif (lindex(text, 0) == "/msg"):
          # /msg target message
          output("-> *%s* %s" % (lindex(text, 1), lrange(text, 2, -1)))
          self.puts_msg(lindex(text, 1), lrange(text, 2, -1))
        
        elif (lindex(text, 0) == "/reload"):
          reload(boredbot)
        else:
          print("ERROR: I don't have that command yet.")
    
      else:
        self.puts_data(text)
        print("> Command executed: %s" % text)









#output("")
#print("Waiting 10secs before close: ", end="")
#for i in range(10, 0, -1):
#  print("%s.. " % i, end="")
#  sys.stdout.flush()
#  time.sleep(1)

