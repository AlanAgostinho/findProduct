import requests
from bs4 import BeautifulSoup
from time import sleep
from decimal import Decimal
import json
import re
from IPython.display import display, HTML
import sys
import codecs
import urllib.request as req
import urllib.parse
import pandas as pd 

def olx(produto, ano = None, cambio = None):
    listing = []
    headers = {
        'user-agent': 'Mozilla/4.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.142 Safari/537.33'}
    html = None
    links = None

    if (cambio != None and ano != None):

        if (cambio == 'manual'):
            cambio = 1
        elif (cambio == 'automatico'):
            cambio = 2
        elif (cambio == 'semi'):
            cambio = 3

        url = 'https://sp.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/{1}?gb={2}&q={0}'.format(produto,ano,cambio)

    elif (cambio != None):

        if (cambio == 'manual'):
            cambio = 1
        elif (cambio == 'automatico'):
            cambio = 2
        elif (cambio == 'semi'):
            cambio = 3

        url = 'https://sp.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios?gb={1}&q={0}'.format(produto,cambio)

    if (ano != None):        
        url = 'https://sp.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/{1}?q={0}'.format(produto,ano)
    else: 
        url = 'https://sp.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios?q={0}'.format(produto)

    r = requests.get(url , headers=headers)

    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        alldata = soup.find_all("li", class_="sc-1fcmfeb-2 ggOGTJ")

        for link in alldata:      
            price = link.find_all("p",  class_="fnmrjs-16 jqSHIm")
            title = link.find("h2", class_="fnmrjs-10 deEIZJ")
            description = link.find("p",  class_="jm5s8b-0 jDoirm")
            
            for links in link.find_all('a'):
                hrfe = links.get('href')

            if (title != None):
                resultado_tmp = '{0}\n{1}\n{2}\n{3}\n'.format(title,price,description,hrfe)
                resultado = [title,price,description,hrfe]

            print((resultado_tmp.replace("</p>","").replace('<h2 class="fnmrjs-10 deEIZJ">','').replace('[<p class="fnmrjs-16 jqSHIm">','').replace('<p class="jm5s8b-0 jDoirm">','').replace('</h2>','').replace(']','')))
            listing.append(resultado)
    return listing

def ml(produto):
    listing = []
    #mercado Livre
    url = 'https://api.mercadolibre.com/sites/MLB/search?q={0}'.format(produto)
    opener = req.build_opener()
    opener.addheaders = [('User-agent',"Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201")]

    with opener.open(url) as fd:
        content = fd.read()
        encoding = fd.info().get_content_charset()
        content = content.decode(encoding)

    dic = json.loads(content)

    sys.stdout = codecs.getwriter('UTF-8')(sys.stdout.detach())
    for elem in dic['results']:
        print('{0:<70}R${1}\n{2}\n{3}\n'.format(elem['title'],
                                            elem['price'],
                                            elem['address'],                                            
                                            elem['permalink']))
        resultado = [elem['title'],elem['price'],elem['address'],elem['permalink']]
        listing.append(resultado)
    return listing


carro = input("coloca o nome do carro: ")
ano = input("coloca o ano do carro: ")

resultado = olx(carro,ano,'manual')
DataFrame = pd.DataFrame(resultado, columns=['Title','Price','Description','HRFE'])
display(DataFrame)

resultado_ml = ml(carro + ano)
DataFrame_ml = pd.DataFrame(resultado_ml, columns=['Title','Price','Description','HRFE'])
# display(DataFrame_ml)

# print(pd.concat([DataFrame,DataFrame_ml]))
