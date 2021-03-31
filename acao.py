import discord
import requests
import os
client = discord.Client()

@client.event
def retornaPrecoAcao():
 async def on_message(message):
    print('teste')
    if message.author == client.user:
        return
    if message.content.startswith('cogna'):
      print('entrou na cogna')
      channel = message.channel
      mensagem = ("COGNA É 15")
      await channel.send(mensagem)
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
        elif(variacao > 0):
          mensagem = ('Preço: R$' + str(precoAgora) + ' - Variação: '   + "{:.2%}".format(variacao)  +  ':chart_with_upwards_trend:')
        else:
          mensagem = ('Preço: R$' + str(precoAgora) + ' - Variação: '   + "{:.2%}".format(variacao) + ' Não houve variação de preço nessa ação até o momento.')
        channel = message.channel
        await channel.send(mensagem)
