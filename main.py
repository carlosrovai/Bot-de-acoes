import os
import time
import json
import random

import discord
import schedule
import tasks
import requests

from keep_alive import keep_alive

client = discord.Client()
URL_ALTA_BAIXA = 'https://www.infomoney.com.br/wp-json/infomoney/v1/highlow'

@client.event
async def on_ready():
    print('Estou vivo ! {0.user}'.format(client))

@client.event
async def on_message(message):  
    if message.author == client.user:
        return

    if 'cogna' in message.content.lower():
        await message.channel.send('COGNA É 15')
    
    if message.content.startswith('$google'):
        mensagem_do_usuario = message.content
        url_formatada = mensagem_do_usuario[8:]
        url_replacada = url_formatada.replace(' ', '+')
        url_google = 'https://www.google.com/search?q=' + url_replacada
        await message.channel.send(url_google)
    elif message.content.startswith('$acao'):
        mensagem_do_usuario = message.content
        msgformatada = mensagem_do_usuario[6:]
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + msgformatada + '.SA?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'
        data = json.loads(requests.get(url))
        preco_atual = float(data['chart']['result'][0]['meta']['regularMarketPrice'])
        ultimo_fechamento = float(data['chart']['result'][0]['meta']['previousClose'])
        variacao = preco_atual/ultimo_fechamento - 1
        if variacao < 0:
            mensagem = f'Preço: R${preco_atual:.2f} - Variação: {variacao:.2%}:chart_with_downwards_trend:'
        elif variacao > 0:
            mensagem = f'Preço: R${preco_atual:.2f} - Variação: {variacao:.2%}:chart_with_upwards_trend:'
        else:
            mensagem = f'Preço: R${preco_atual:.2f} - Variação: {variacao:.2%} Não houve variação de preço nessa ação até o momento.'
        await message.channel.send(mensagem)
    elif message.content.startswith('$acoesalta'):
        data = json.loads(requests.get(URL_ALTA_BAIXA))
        mensagem = ''
        for i in range(5):
          acao = str(data['high'][i]['StockCode'])
          preco = float(data['high'][i]['VALOR'])
          oscilacao = float(data['high'][i]['OSCILACAO'])
          mensagem += f'Ação: {acao}     Preço atual: R$ {preco:.2f} Variação: {oscilacao:.2f}%:chart_with_upwards_trend:\n'
        await message.channel.send(mensagem)
    elif message.content.startswith('$acoesbaixa'):
        data = json.loads(requests.get(URL_ALTA_BAIXA))
        mensagem = ''
        for i in range(5):
          acao = str(data['low'][i]['StockCode'])
          preco = float(data['low'][i]['VALOR'])
          oscilacao = float(data['low'][i]['OSCILACAO'])
          mensagem += f'Ação: {acao}     Preço atual: R$ {preco:.2f} Variação: {oscilacao:.2f}%:chart_with_downwards_trend:\n'
        await message.channel.send(mensagem)

keep_alive()
client.run(os.getenv('keybot'))
