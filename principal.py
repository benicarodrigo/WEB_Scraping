from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep
import pandas as pd
from os import path
from platform import system


lst_nome_ativo = []
lst_valor_abertura = []
lst_valor_maximo = []
lst_valor_minimo = []
lst_fechamento = []
lst_volume = []

so = system()


count = 0
df_emp_alta = pd.DataFrame(columns=['Emresa', 'Valor Abertura', 'Valor Maximo', 'Valor Minimo', 'Fechamento', 'Volume'])
df_emp_baixa = pd.DataFrame(columns=['Emresa', 'Valor Abertura', 'Valor Maximo', 'Valor Minimo', 'Fechamento', 'Volume'])
url = 'https://statusinvest.com.br/acoes/variacao/ibov'
path = path.dirname(__file__)

if so == 'Linux':
    path_driver = path + '/chromedriver'
else:
    path_driver = path + '/chromedriver.exe'



driver_gc = webdriver.Chrome(path_driver)
driver_gc.get(url)
sleep(3)
bs_obj_url = bs(driver_gc.page_source, 'html.parser')

#Captura os links para empresas que tiveram alta e baixa
tab_altabaixa = bs_obj_url.find_all('li', {'class': 'tab'})
link_altabaixa = [tab.find('a').get('href') for tab in tab_altabaixa]


bs_obj_url = bs(driver_gc.page_source, 'html.parser')
list_empresas = bs_obj_url.find_all('a', {'class': 'waves-effect waves-on-white-bg'})
qtd_alta = int(bs_obj_url.find('strong', {'class': 'bg-main d-inline-block fs-2 lh-3 pl-1 pr-1 quantity rounded white-text'}).text)

if qtd_alta >= 5:
    list_empresas_alta = list_empresas[0:5]
    list_empreas_baixa = list_empresas[qtd_alta:qtd_alta + 5]

else:
    list_empresas_alta = list_empresas[0:qtd_alta]
    list_empreas_baixa = list_empresas[qtd_alta + 1:qtd_alta + 5]

for emp in list_empresas_alta:

    nome_ativo = emp.find('small',{'title':'Nome da empresa/FII'})
    valor_abertura = emp.find('div',{'title':'Valor de abertura'})
    valor_abertura_val = valor_abertura.find('span', {'class': 'value'}).text
    valor_maximo = emp.find('div',{'title':'Máxima do dia'})
    valor_maximo_val = valor_maximo.find('span', {'class': 'value'}).text
    valor_minimo = emp.find('div', {'title': 'Mínima do dia'})
    valor_minimo_val = valor_minimo.find('span', {'class': 'value'}).text
    fechamento = emp.find('div', {'title': 'Valor de fechamento'})
    fechamento_val = fechamento.find('span', {'class': 'value'}).text
    volume = emp.find('div', {'title': 'Volume financeiro'})
    volume_val = volume.find('span', {'class': 'value'}).text

    lst_nome_ativo.append(nome_ativo)
    lst_valor_abertura.append(valor_abertura_val)
    lst_valor_maximo.append(valor_maximo_val)
    lst_valor_minimo.append(valor_minimo_val)
    lst_fechamento.append(fechamento_val)
    lst_volume.append(volume_val)

dc_emp_alta = {'Emresa': lst_nome_ativo , 'Valor Abertura': lst_valor_abertura , 'Valor Maximo': lst_valor_maximo, 'Valor Minimo' : lst_valor_minimo, 'Fechamento': lst_fechamento, 'Volume': lst_volume}
df_emp_alta = pd.DataFrame(data=dc_emp_alta)

lst_nome_ativo.clear()
lst_fechamento.clear()
lst_valor_abertura.clear()
lst_valor_maximo.clear()
lst_valor_minimo.clear()
lst_volume.clear()

for emp in list_empreas_baixa:

    nome_ativo = emp.find('small', {'title': 'Nome da empresa/FII'})
    valor_abertura = emp.find('div', {'title': 'Valor de abertura'})
    valor_abertura_val = valor_abertura.find('span', {'class': 'value'}).text
    valor_maximo = emp.find('div', {'title': 'Máxima do dia'})
    valor_maximo_val = valor_maximo.find('span', {'class': 'value'}).text
    valor_minimo = emp.find('div', {'title': 'Mínima do dia'})
    valor_minimo_val = valor_minimo.find('span', {'class': 'value'}).text
    fechamento = emp.find('div', {'title': 'Valor de fechamento'})
    fechamento_val = fechamento.find('span', {'class': 'value'}).text
    volume = emp.find('div', {'title': 'Volume financeiro'})
    volume_val = volume.find('span', {'class': 'value'}).text

    lst_nome_ativo.append(nome_ativo)
    lst_valor_abertura.append(valor_abertura_val)
    lst_valor_maximo.append(valor_maximo_val)
    lst_valor_minimo.append(valor_minimo_val)
    lst_fechamento.append(fechamento_val)
    lst_volume.append(volume_val)

dc_emp_baixa = {'Emresa': lst_nome_ativo , 'Valor Abertura': lst_valor_abertura , 'Valor Maximo': lst_valor_maximo, 'Valor Minimo' : lst_valor_minimo, 'Fechamento': lst_fechamento, 'Volume': lst_volume}
df_emp_baixa = pd.DataFrame(data=dc_emp_baixa)

print('Empreas em alta')
print(df_emp_alta)

print('Empreas em baixa')
print(df_emp_baixa)


driver_gc.quit()