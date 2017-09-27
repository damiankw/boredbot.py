class nickname:
  # can add things in here like last seen and all that jargon, but required are nick, user, host, name

  def __init__(self, nick, user, host, name):
    self.INFO = {
      'nick': nick,
      'user': user,
      'host': host,
      'name': name
    }
  
  def nick(self):
    return self.INFO['nick']
  
  def user(self):
    return self.INFO['user']
  
  def host(self):
    return self.INFO['host']
  
  def name(self):
    return self.INFO['name']
  
  def uhost(self):
    return self.INFO['user'] + "@" + self.INFO['host']
  
  def update(self, item, value):
    self.INFO[item] = value
    
  def __str__(self):
    return "%s!%s@%s" % (self.INFO['nick'], self.INFO['user'], self.INFO['host'])
  

class nicklist:
  # ul.add(nick, user, host, real name) - add user to the list
  # ul.del(nick) - delete user from the list
  # ul.get(nick) - get full dict of user
  # ul.update(nick, field, value) - update a field for a user
  
  def __init__(self):
    self.LIST = {}
  
  
  def list(self):
    return list(self.LIST)

  def get(self, nick):
    if not (nick.lower() in self.LIST): # the nick doesnt exist
      return None

    else: # print whole list
      return self.LIST[nick.lower()]
  
  def add(self, nick, user=None, host=None, name=None): # add a new nickname into the mix
    if (isinstance(nick, nickname)): # if the nick is actually a nickname()
      self.LIST[nick.nick().lower()] = nick
      return True

    elif (nick.lower() in self.LIST): # check if the nickname already exists
      return None

    else:
      self.LIST[nick.lower()] = nickname(nick, user, host, name)
      return True
  
  def remove(self, nick):
    if not (nick.lower() in self.LIST):
      return None

    else:
      del(self.LIST[nick.lower()])
      return True

  def update(self, nick, item, value):
    if not (nick.lower() in self.LIST):
      return None

    else:
      self.LIST[nick.lower()].update(item, value)
      return True
