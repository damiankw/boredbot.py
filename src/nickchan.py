class nickchan:
  def __init__(self):
    self.LIST = {}
    
  def add(self, nick, chan): # add an item in
    self.LIST[nick.lower() + ',' + chan.lower()] = ""
    return True
    
  def remove(self, nick, chan): # take an item out
    if (nick.lower() + ',' + chan.lower() in self.LIST):
      del(self.LIST[nick.lower() + ',' + chan.lower()])
      return True
    else:
      return False
    
  def get_chan(self, nick): # get the users in a channel
    chans = {}
    for item in self.LIST.items(): # loop through all matches
      newitem = item[0].split(",") # explode so we can search nick/chan
      
      if (newitem[0].lower() == nick.lower()): # check if we're on the right nickname
        chans[newitem[1]] = item[1]
    
    if (len(chans) == 0):
      return None
    
    return list(chans)

  def get_nick(self, chan, mode=None): # get the channels a user is on
    nicks = {}
    for item in self.LIST.items(): # loop through all matches
      newitem = item[0].split(",") # explode so we can search nick/chan
      
      if (newitem[1].lower() == chan.lower()): # check if we're on the right nickname
        if (mode is None) or (mode in item[1]):
          nicks[newitem[0]] = item[1]
    
    if (len(nicks) == 0):
      return None
    
    return list(nicks)
    
  def set_mode(self, nick, chan, mode): # set the mode of the user
    if (nick.lower() + ',' + chan.lower() in self.LIST):
      self.LIST[nick.lower() + ',' + chan.lower()] = mode
  
  def get_mode(self, nick, chan): # get the mode of user in a channel
    if (nick.lower() + ',' + chan.lower() in self.LIST):
     return self.LIST[nick.lower() + ',' + chan.lower()]

  def list(self):
    return list(self.LIST)

  def __str__(self):
    return str(self.LIST)
  
  
  
  
  
  
  
  
  
  
  
  
  