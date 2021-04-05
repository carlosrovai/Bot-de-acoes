import discord
import os
import json
import requests
import random
from keep_alive import keep_alive

client = discord.Client()
urlaltabaixa = 'https://www.infomoney.com.br/wp-json/infomoney/v1/highlow'

@client.event
async def on_ready():
    print('i am alive {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if ('cogna' in message.content):
        channel = message.channel
        mensagem = ("COGNA É 15")
    if message.content.startswith('$google'):
        mensagemDoUsuario = message.content
        urlformatada = (mensagemDoUsuario[8:])
        urlreplacada = urlformatada.replace(" ", "+")
        urlGoogle = 'https://www.google.com/search?q=' + urlreplacada
        channel = message.channel
        await channel.send(urlGoogle)
    if message.content.startswith('$acao'):
        mensagemDoUsuario = message.content
        msgformatada = (mensagemDoUsuario[6:])
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + msgformatada + '.SA?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'
        data = (requests.get(url))
        precoAgora = float(
            (data.json()['chart']['result'][0]['meta']['regularMarketPrice']))
        precoAntesDeFechar = float(
            (data.json()['chart']['result'][0]['meta']['previousClose']))
        variacao = float((precoAgora / precoAntesDeFechar) - 1)
        if (variacao < 0):
            mensagem = ('Preço: R$' + str(precoAgora) + ' - Variação: ' +
                        "{:.2%}".format(variacao) +
                        ':chart_with_downwards_trend:')
        elif (variacao > 0):
            mensagem = ('Preço: R$' + str(precoAgora) + ' - Variação: ' +
                        "{:.2%}".format(variacao) +
                        ':chart_with_upwards_trend:')
        else:
            mensagem = (
                'Preço: R$' + str(precoAgora) + ' - Variação: ' +
                "{:.2%}".format(variacao) +
                ' Não houve variação de preço nessa ação até o momento.')
        channel = message.channel
    if message.content.startswith('$acoesalta'):
        channel = message.channel
        data = (requests.get(urlaltabaixa))
        i = 0
        mensagem = ''
        while (i < 5 ):
          acao = str(data.json()['high'][i]['StockCode'])
          preco = str(data.json()['high'][i]['VALOR'])
          oscilacao = float(data.json()['high'][i]['OSCILACAO'])/100
          mensagem = mensagem + str(('Ação: '  +acao+ '     Preço atual: R$ '+str(preco)) + ' Variação: ' + "{:.2%}".format(oscilacao) + ':chart_with_upwards_trend:' '\n')
          i = i + 1
    if message.content.startswith('$acoesbaixa'):
        channel = message.channel
        data = (requests.get(urlaltabaixa))
        i = 0
        mensagem = ''
        while (i < 5 ):
          acao = str(data.json()['low'][i]['StockCode'])
          preco = str(data.json()['low'][i]['VALOR'])
          oscilacao = float(data.json()['low'][i]['OSCILACAO'])/100
          mensagem = mensagem + str(('Ação: '  +acao+ '     Preço atual: R$ '+str(preco)) + ' Variação: ' + "{:.2%}".format(oscilacao) + ':chart_with_downwards_trend:' '\n')
          i = i + 1    
    await channel.send(mensagem)


keep_alive()
client.run(os.getenv('keybot'))
