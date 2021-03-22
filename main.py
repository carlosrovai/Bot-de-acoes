import discord
import os
import json
import requests
import random

client = discord.Client()


@client.event
async def on_ready():
    print('i am alive {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #if message.content.startswith == '$acao' + acaoEscolhida:
    if message.content.startswith('$seal'):
      focas = ["https://i.imgur.com/ll23fBf.jpg", "https://i.imgur.com/njyzIzI.jpg","https://i.imgur.com/E6I1DcN.png","https://i.imgur.com/7loGQVj.jpg"]
      channel = message.channel
      await channel.send(focas[random.randint(0,3)])
      print(focas[0])
      print(focas[1])
      print(focas[2])
      print(focas[4])
    if message.content.startswith('$google'):
      mensagemDoUsuario = message.content
      urlformatada = (mensagemDoUsuario[8:])
      urlreplacada = urlformatada.replace(" ","+")
      urlGoogle = 'https://www.google.com/search?q='+ urlreplacada
      channel = message.channel
      await channel.send(urlGoogle)
    if message.content.startswith('$acao'):
        mensagemDoUsuario = message.content
        msgformatada = (mensagemDoUsuario[6:])
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + msgformatada + '.SA?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'
        data = (requests.get(url))
        precoAgora = float((
            data.json()['chart']['result'][0]['meta']['regularMarketPrice']))
        precoAntesDeFechar = float((
            data.json()['chart']['result'][0]['meta']['previousClose']))
        variacao = float((precoAgora / precoAntesDeFechar) - 1)
        if (variacao < 0):
            mensagem = ('Preço: R$' + str(precoAgora) + ' - Variação: ' + "{:.2%}".format(variacao)  + ':chart_with_downwards_trend:')
        else:
          mensagem = ('Preço: R$' + str(precoAgora) + ' - Variação: '   + "{:.2%}".format(variacao)  +  ':chart_with_upwards_trend:')
            

        channel = message.channel
        await channel.send(mensagem)


client.run(os.getenv('keybot'))
