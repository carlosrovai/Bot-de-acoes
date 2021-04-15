import os
import json
import random
import discord
import requests

URL_ALTA_BAIXA = 'https://www.infomoney.com.br/wp-json/infomoney/v1/highlow'

def url_google_para(uma_pesquisa):
  url_replacada = uma_pesquisa.replace(' ', '+')
  url_google = 'https://www.google.com/search?q=' + url_replacada
  return url_google

def mensagem_para_comando_acao(um_simbolo_de_acao):
  url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + um_simbolo_de_acao + '.SA?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'
  data = requests.get(url).json()
  preco_atual = float(data['chart']['result'][0]['meta']['regularMarketPrice'])
  ultimo_fechamento = float(data['chart']['result'][0]['meta']['previousClose'])
  variacao = preco_atual/ultimo_fechamento - 1
  if variacao < 0:
      mensagem = f'Preço: R${preco_atual:.2f} - Variação: {variacao:.2%}:chart_with_downwards_trend:'
  elif variacao > 0:
      mensagem = f'Preço: R${preco_atual:.2f} - Variação: {variacao:.2%}:chart_with_upwards_trend:'
  else:
      mensagem = f'Preço: R${preco_atual:.2f} - Variação: {variacao:.2%} Não houve variação de preço nessa ação até o momento.'
  return mensagem

def mensagem_para_comando_acoesalta():
  data = requests.get(URL_ALTA_BAIXA).json()
  mensagem = ''
  for i in range(5):
    acao = str(data['high'][i]['StockCode'])
    preco = float(data['high'][i]['VALOR'])
    oscilacao = float(data['high'][i]['OSCILACAO'])
    mensagem += f'Ação: {acao}     Preço atual: R$ {preco:.2f} Variação: {oscilacao:.2f}%:chart_with_upwards_trend:\n'
  return mensagem

def mensagem_para_comando_acoesbaixa():
  data = requests.get(URL_ALTA_BAIXA).json()
  mensagem = ''
  for i in range(5):
    acao = str(data['low'][i]['StockCode'])
    preco = float(data['low'][i]['VALOR'])
    oscilacao = float(data['low'][i]['OSCILACAO'])
    mensagem += f'Ação: {acao}     Preço atual: R$ {preco:.2f} Variação: {oscilacao:.2f}%:chart_with_downwards_trend:\n'
  return mensagem

def funcao(message):
  if message.content.startswith('$google'):
    pesquisa = message.content[8:]
    return url_google_para(pesquisa)
  elif message.content.startswith('$acao'):
    simbolo_de_acao = message.content[6:]
    return mensagem_para_comando_acao(simbolo_de_acao)
  elif message.content.startswith('$acoesalta'):
    return mensagem_para_comando_acoesalta()
  elif message.content.startswith('$acoesbaixa'):
    return mensagem_para_comando_acoesbaixa()

  return None