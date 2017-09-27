# import common
import sys
import os # for changing the folder
os.chdir(os.path.dirname(sys.argv[0]))

# import custom
from boredbot import *


CONFIG = {
  'server': '10.0.0.25',
  'port': 6667,
  'nick': 'damibawt',
  'ident': 'damibawt',
  'name': 'A robot!',
  'cmd': '.'
}

bot = boredbot(CONFIG)
bot.connect()

bot.catch()