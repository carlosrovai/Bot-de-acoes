import requests

URL_ALTA_BAIXA = 'https://www.infomoney.com.br/wp-json/infomoney/v1/highlow'

def url_google_para(uma_pesquisa):
  url_replacada = uma_pesquisa.replace(' ', '+')
  url_google = 'https://www.google.com/search?q=' + url_replacada
  return url_google
def mensagem_para_comando_acao(um_simbolo_de_acao): 
  acoes = um_simbolo_de_acao.split(' ')
  mensagem = ''
  for acao in acoes:
   url = 'https://query1.finance.yahoo.com/v8/finance/chart/' + acao + '.SA?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'
   data = requests.get(url).json()
   preco_atual = float(data['chart']['result'][0]['meta']['regularMarketPrice'])
   ultimo_fechamento = float(data['chart']['result'][0]['meta']['previousClose'])
   variacao = preco_atual/ultimo_fechamento - 1
   if variacao < 0:
      mensagem += f'`Ação: {acao.upper()} Preço: R${preco_atual:.2f}  - Variação:{variacao:.2%}`:chart_with_downwards_trend: \n'
   elif variacao > 0:
      mensagem +=  f'`Ação: {acao.upper()} Preço: R${preco_atual:.2f}  - Variação:{variacao:.2%}`:chart_with_upwards_trend: \n'
   else:
      mensagem += f'`Ação: {acao.upper()} Preço: R${preco_atual:.2f} - Variação: {variacao:.2%} Não houve variação de preço nessa ação até o momento. `\n'
  return mensagem

def mensagem_para_comando_acoesalta():
  data = requests.get(URL_ALTA_BAIXA).json()
  mensagem = ''
  ranking = 1
  for i in range(5):
    acao = str(data['high'][i]['StockCode'])
    preco = float(data['high'][i]['VALOR'])
    oscilacao = float(data['high'][i]['OSCILACAO'])
    mensagem += f'`{ranking}º Ação:{acao:6}   Preço atual:R${preco:>5.2f}   Variação:{oscilacao:.2f}%`:chart_with_upwards_trend:\n'
    ranking = ranking + 1
  return mensagem

def mensagem_para_comando_acoesbaixa():
  data = requests.get(URL_ALTA_BAIXA).json()
  mensagem = ''
  ranking = 1
  for i in range(5):
    acao = str(data['low'][i]['StockCode'])
    preco = float(data['low'][i]['VALOR'])
    oscilacao = float(data['low'][i]['OSCILACAO'])
    mensagem += f'`{ranking}º Ação:{acao:6}   Preço atual:R${preco:>5.2f}   Variação:{oscilacao:.2f}%`:chart_with_downwards_trend:\n'
    ranking = ranking + 1
  return mensagem

def mensagem_para_comando_ada():
  url = 'https://query1.finance.yahoo.com/v8/finance/chart/ADA-USD?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'
  data = requests.get(url).json()
  preco = float(data['chart']['result'][0]['meta']['regularMarketPrice']) 
  mensagem = f'O preço atual do ADA é de R${preco*dolar():.2f} '
  return mensagem
  
def dolar():
  url = 'https://economia.awesomeapi.com.br/json/last/usd-brl'
  data = requests.get(url).json()
  preco_dolar = float(data['USDBRL']['ask'])
  mensagem = f'O valor do dolar em reais é R${preco_dolar:.2f}'
  print(mensagem)
  return preco_dolar

def mensagem_para_comando_acaoinfo(argumento):
  infos = {
    'cogn3': 'Cogna Educacao SA',
    'mglu3': 'Magazine Luiza SA',
    'tsla34': 'Tesla Motors Inc BDR',
  }
  resultado = ''
  if '--ajuda' in argumento:
    resultado += '''**Comando**:
\t\t$acaoinfo
*Descrição*:
\t\tMostra informações sobre uma ou mais ações.
__Autor__:
\t\tGabriel Araujo
~~Exemplos de uso:~~
\t\t`$acaoinfo cogn3`
\t\t`$acaoinfo mglu3 tsla34 petr4`
\t\t`$acaoinfo --todas`
\t\t`$acaoinfo --ajuda`'''
  elif '--todas' in argumento:
    for acao, info in infos.items():
      resultado += f"`{acao.upper():6} | {info}`\n"
  else:
    acoes = argumento.split()
    for acao in acoes:
      acao_info = infos.get(acao.lower(), None)
      if acao_info is None:
        resultado += f"`{acao.upper():6} | Ainda não temos informações sobre esta ação!`\n"
      else:
        resultado += f"`{acao.upper():6} | {acao_info}`\n"
  return resultado

def funcao(message):
  if message.content.startswith('$google '):
    pesquisa = message.content[8:]
    return url_google_para(pesquisa)
  elif message.content.startswith('$acao '):
    simbolo_de_acao = message.content[6:]
    return mensagem_para_comando_acao(simbolo_de_acao)
  elif message.content.startswith('$acoesalta'):
    return mensagem_para_comando_acoesalta()
  elif message.content.startswith('$acoesbaixa'):
    return mensagem_para_comando_acoesbaixa()
  elif message.content.startswith('$ada'):
    return mensagem_para_comando_ada()
  elif message.content.startswith('$dolar'):
    return  f'O valor do dolar em reais é R${dolar():.2f}'
  elif message.content.startswith('$acaoinfo '):
    argumento = message.content[10:]
    return mensagem_para_comando_acaoinfo(argumento)
  return None
