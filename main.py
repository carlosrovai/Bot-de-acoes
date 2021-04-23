import os

import discord

from acao import funcao
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
    print('Estou vivo ! {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if 'cogna' in message.content.lower():
    await message.channel.send('COGNA É 15')

  try:
    mensagem = funcao(message)
    if mensagem is not None:
      await message.channel.send(mensagem)
  except:
    mensagem = 'escreve certo burro'
    await message.channel.send(mensagem)

keep_alive()
client.run(os.getenv('keybot'))
