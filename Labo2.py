#2. Laborategia ANDONI OLABARRIA (eGelako Web Sistema orriaren PDF-ak deskargatu)
import psutil
import time
import signal
import sys
import requests
import urllib
import json
import getpass
from bs4 import BeautifulSoup

#Login token eta Cookie-a lortzeko eskaera
def eskaera1():
    metodoa = 'GET'
    uria = "https://egela.ehu.eus/login/index.php"
    goiburuak = {'Host': 'egela.ehu.eus'}
    erantzuna = requests.request(metodoa, uria,
                                 headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    html = erantzuna.content
    # bilaketaren emaitzak dituen HTML dokumentua parseatu
    soup = BeautifulSoup(html, 'html.parser')
    login_token = soup.find_all('td', {'class': 'fondo_listado'})
    cookie = soup.find_all('td', {'class': 'fondo_listado'})
    #soup.find_all PROBA

if __name__ == '__main__':
    #Programa deitzerakoan argumentuak 1: erabiltzailea 2: izena
    a = str(sys.argv[1])
    b = str(sys.argv[2])
    print('Kaixo ' + b + ' // Erabiltzailea: ' + a )
    #eGela-ko erabiltzailearen pasahitza getpass bidez lortu
    psw = getpass.getpass(prompt='Pasahitza sartu: ')
    eskaera1()