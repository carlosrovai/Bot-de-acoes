import discord
import os
import json
import requests
import random
from keep_alive import keep_alive
from acao import retornaPrecoAcao

client = discord.Client()

@client.event
async def on_ready():
    print('i am alive {0.user}'.format(client))

retornaPrecoAcao()

keep_alive()
client.run(os.getenv('keybot'))
