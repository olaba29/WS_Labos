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
    print(' ')
    print(' - 1. Eskaeraren INFO: - ')
    print("URI: " + uria)
    print(' - 1. Erantzunaren INFO: - ')
    print(str(kodea) + " " + deskribapena)
    print(' --------------------------- ')
    html = erantzuna.content
    # bilaketaren emaitzak dituen HTML dokumentua parseatu
    soup = BeautifulSoup(html, 'html.parser')
    login_token = soup.find('input', {'name':'logintoken'})['value']
    print('Login token: ' + login_token)
    cookie = erantzuna.headers['Set-Cookie'].split(";")[0]
    print('Cookie-a: ' + cookie)
    location = soup.find('form', {'class':'m-t-1 ehuloginform'})['action']
    print('Location: + location')
    data = [login_token, cookie, location]
    return data

def eskaera2(cookie, logintoken, location, erabiltzailea, psw):
    metodoa = 'POST'
    uria = location
    goiburuak = {'Host': 'egela.ehu.eus', 'Cookie':cookie, 'Content-Type':'application/x-www-form-urlencoded'}
    data = 'logintoken=' + str(logintoken) + '&username=' + str(erabiltzailea) + '&password=' + str(psw)
    edukia = {data}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia_encoded,
                                 headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(' ')
    print(' - 2. Eskaeraren INFO: - ')
    print("URI: " + uria)
    print(' - 2. Erantzunaren INFO: - ')
    print(str(kodea) + " " + deskribapena)
    print(' --------------------------- ')
    print(data)
    html = erantzuna.content
    # bilaketaren emaitzak dituen HTML dokumentua parseatu
    soup = BeautifulSoup(html, 'html.parser')
    #moodleSessionegela eta location nahi dira erantzunetik lortu
    cookie = erantzuna.headers['Set-Cookie'].split(";")[0]
    print('Cookie-a: ' + cookie)
    location = soup.find('form', {'class': 'm-t-1 ehuloginform'})['action']
    print('Location: + location')
    data2 = [ cookie, location]
    return data2

if __name__ == '__main__':
    #Programa deitzerakoan argumentuak 1: erabiltzailea 2: izena
    a = str(sys.argv[1])
    b = str(sys.argv[2])
    print('Kaixo ' + b + ' // Erabiltzailea: ' + a )
    #eGela-ko erabiltzailearen pasahitza getpass bidez lortu
    psw = getpass.getpass(prompt='Pasahitza sartu: ')
    # -- Lehen eskaera --
    datuak1e=eskaera1()
    logintoken1 = datuak1e[0]
    cookie1 = datuak1e[1]
    location1 = datuak1e[2]
    # -- Bigarren eskaera --
    datuak2e = eskaera2(cookie1,logintoken1,location1,a,psw)
