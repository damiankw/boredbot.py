class channel:
  # can add things in here like last seen and all that jargon, but required are chan, user, host, name
  INFO = {}
  INFO['topic'] = "" # current topic (topic, by, date)
  INFO['created'] = "" # when the channel was created on the server
  INFO['mode'] = "" # the current modes
  INFO['joined'] = "" # when the bot joined
  

  def __init__(self, chan):
    self.INFO['chan'] = chan
  
  def chan(self):
    return self.INFO['chan']
  
  def topic(self):
    return self.INFO['topic']
  
  def set_topic(self, topic):
    self.INFO['topic']['topic'] = topic
    
  def set_topic_user(self, nick):
    self.INFO['topic']['nick'] = nick
    
  def set_topic_date(self, date):
    self.INFO['topic']['date'] = date
  
  def created(self):
    return self.INFO['created']
  
  def mode(self):
    return self.INFO['mode']
  
  def joined(self):
    return self.INFO['joined']
  
  def update(self, item, value):
    self.INFO[item] = value
    
  def __str__(self):
    return self.INFO['chan']
  

class chanlist:
  # ul.add(chan, user, host, real name) - add user to the list
  # ul.del(chan) - delete user from the list
  # ul.get(chan) - get full dict of user
  # ul.update(chan, field, value) - update a field for a user
  
  def __init__(self):
    self.LIST = {}
  
  
  def list(self):
    return list(self.LIST)

  def get(self, chan):
    if not (chan.lower() in self.LIST): # the chan doesnt exist
      return None

    else: # print whole list
      return self.LIST[chan.lower()]
  
  def add(self, chan): # add a new channel into the mix
    if (isinstance(chan, channel)): # if the chan is actually a channel()
      self.LIST[chan.chan().lower()] = chan
      return True

    elif (chan.lower() in self.LIST): # check if the channel already exists
      return None

    else:
      self.LIST[chan.lower()] = channel(chan)
      return True
  
  def remove(self, chan):
    if not (chan.lower() in self.LIST):
      return None

    else:
      del(self.LIST[chan.lower()])
      return True

  def update(self, chan, item, value):
    if not (chan.lower() in self.LIST):
      return None

    else:
      self.LIST[chan.lower()].update(item, value)
      return True

