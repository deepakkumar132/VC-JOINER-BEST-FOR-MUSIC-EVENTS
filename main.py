
import os
os.system("pip install websocket-client")
import websocket
import discord
import requests
import sys
import json
from typing import Optional
import asyncio
import threading
from json import dumps
from colorama import Fore, init
import time

init(convert=True)

def Clear():
  if sys.platform in ["linux", "linux2"] or os.name == "posix":
    if not os.name == "nt":
      os.system("clear")
    else:
      os.system("cls")
  else:
    os.system('cls')

def setTitle(title: Optional[any]=None):
  os.system("title "+title)

setTitle("VC Joiner & Token Hoster");Clear()
print(f'''
                              \033[91m████████╗███████╗░█████╗░███╗░░░███╗░░░░░░░█████╗░██╗\033[39m
                              \033[91m╚══██╔══╝██╔════╝██╔══██╗████╗░████║░░░░░░██╔══██╗██║\033[39m
                              \033[91m░░░██║░░░█████╗░░███████║██╔████╔██║█████╗███████║██║\033[39m
                              \033[91m░░░██║░░░██╔══╝░░██╔══██║██║╚██╔╝██║╚════╝██╔══██║██║\033[39m
                              \033[91m░░░██║░░░███████╗██║░░██║██║░╚═╝░██║░░░░░░██║░░██║██║\033[39m
                              \033[91m░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░░░░╚═╝░░╚═╝╚═╝\033[39m
''')
tokens = []
verify_tken = []
unchecked_tokens = []
session = requests.Session()
url = "https://discord.com/api/v9/users/@me"

def Check_Tokens(token):
  req = session.get(url=url, headers={"Authorization": token})
  if req.status_code in [204, 200, 201, 299]:
    if "need to verify" in req.text:
      print(f"{token} Unverified Token.")
      verify_tken.append(token)
    else:
      tokens.append(token)
  elif req.status_code in [499, 404, 401, 400]:
    print("{} Is Invaild Token And Removed From List.".format(token))


for token in open('tokens.txt', 'r').readlines():
  tk = token.strip()
  unchecked_tokens.append(tk)

for token in unchecked_tokens:
  Check_Tokens(token)

all_tkens = []

for token in verify_tken:
  all_tkens.append(token)
for tk in tokens:
  all_tkens.append(tk)

with open('config.json') as config_file:
  nig = json.load(config_file)


status = nig["Status"]
st = status.lower()
activity = nig['Activity']
tyy = activity.lower()
name = nig['Activity_Name']
guild = nig['Guild_ID']
vc = nig['Voice_Channel_ID']

if st == "idle":
  ust = discord.Status.idle
elif st == "dnd":
  ust = discord.Status.dnd
elif st == "online":
  ust = discord.Status.online

if tyy == "streaming":
  acttt = discord.Streaming(name=name, url="Streaming")
elif tyy == "playing":
  acttt = discord.Game(name=name)
elif tyy == "listening":
  acttt=discord.Activity(type=discord.ActivityType.listening, name=name)
elif tyy == "watching":
  acttt=discord.Activity(type=discord.ActivityType.watching, name=name)
akks = []
loop = asyncio.get_event_loop()

banner = f"""{Fore.RED}[-]{Fore.RESET}Ai-Deepak-17."""

useless_shit = f"""{Fore.RED}[-]{Fore.RESET}\n\n{Fore.GREEN}[+]{Fore.RESET} Sucessfully Hosted All Tokens & Joined Voice Channel"""

print(banner)

def task_(Token):
  ws = websocket.WebSocket()
  ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
  ws.send(dumps({"op": 2,"d": {"token": Token, "properties": {"$os": "windows","$browser": "Discord","$device": "desktop"}}}))
  ws.send(dumps({"op": 4,"d": {"guild_id": guild,"channel_id": vc, "self_mute": True,"self_deaf": True}}))


for tk in all_tkens:
  intents = discord.Intents.default()
  intents.typing = False 
  client = discord.Client(intents=intents, status=ust, activity=acttt)
  #client = discord.Client(status=ust, activity=acttt)
  loop.create_task(client.start(tk))
  akks.append(client)
  print(" ")
  print("{} Is Hosted.\n".format(tk))

threading.Thread(target=loop.run_forever).start()


time.sleep(5)
Clear()
print(useless_shit)
while True:
  for tk_ in tokens:
    task_(tk_)