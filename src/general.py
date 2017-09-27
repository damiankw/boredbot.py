# these are functions for general purpose
import time
import re
import colorama

from colorama import Fore, Back, Style
colorama.init()

def output(text, show_time=True):
  if (show_time == True):
    print("[%s] %s" % (time.strftime('%H:%M:%S'), text))
  else:
    print("%s" % text)

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

def removeslashes(s):
  # thanks to http://www.php2python.com/wiki/function.addslashes/
    s = s.replace('\\"', '"').replace('\\\'', '\'').replace('\\\\', '\\')
    return s

def split_fulladdress(address):
  if (re.match(".+!.+@.+", address)):
    return address.replace("!", " ").replace("@", " ").split(" ")
  else:
    return [address, "", ""]

def mask(address, type):
  nick = address.split("!")[0]
  user = address.split("!")[1].split("@")[0]
  host = address.split("!")[1].split("@")[1]
  
  if (type == 1):
    # *!*damian@damian.id.au
    return "*!*%s@%s" % (user.strip("*"), host)
    
  elif (type == 2):
    # *!*@damian.id.au
    return "*!*@%s" % (host)
    
  elif (type == 3):
    # *!*damian@*.id.au
    return "*!*%s@*.%s" % (user.strip("*"), ".".join(host.split(".")[1:]))
    
  elif (type == 4):
    # *!*@*.id.au
    return "*!*@*.%s" % (".".join(host.split(".")[1:]))
    
  elif (type == 5):
    # damian!damian@damian.id.au
    return "%s!%s@%s" % (nick, user, host)
    
  elif (type == 6):
    # damian!*damian@damian.id.au
    return "%s!*%s@%s" % (nick, user.strip("*"), host)
    
  elif (type == 7):
    # damian!*@damian.id.au
    return "%s!*@%s" % (nick, host)
    
  elif (type == 8):
    # damian!*damian@*.id.au
    return "%s!*%s@*.%s" % (nick, user.strip("*"), ".".join(host.split(".")[1:]))
    
  elif (type == 9):
    # damian!*@*.id.au
    return "%s!*@*.%s" % (nick, ".".join(host.split(".")[1:]))
    
  elif (type == 10):
    # *!damian@damian.id.au
    return "*!%s@%s" % (user, host)
  
def mode_def():
  # set a default set of modes in case the server doesn't have them (or rather, if i don't put it into the code)
  return {'h': '%', 'v': '+', 'o': '@'}

def mode2char(mode, modes=0):
  if (modes == 0):
    modes = mode_def()
  
  if (mode in modes):
    return modes[mode]
  else:
    return ""
    
def char2mode(char, modes=0):
  if (modes == 0):
    modes = mode_def()
  
  for mode in modes:
    if (modes[mode] == char):
      return mode
  else:
    return ""
  
def is_mode(mode, modes=0):
  if (modes == 0):
    modes = mode_def()
  
  if (mode in modes.values()):
    return True
  else:
    return False


############## colours
# 0 - White | WHITE
# 1 - Black | BLACK
# 2 - Navy
# 3 - Green
# 4 - Red
# 5 - Dark Red | RED
# 6 - Purple | MAGENTA
# 7 - Orange
# 8 - Yellow
# 9 - Bright Green
# 10 - Aqua
# 11 - Cyan | CYAN
# 12 - Blue | BLUE
# 13 - Magenta
# 14 - Dark Grey
# 15 - Grey

def col2chr(colour):
  # this will convert colorama.COLOR into ^Cn
  print("d")
  
def chr2col(chr):
  # this will convert ^Cn to colorama.COLOR
  print("d")