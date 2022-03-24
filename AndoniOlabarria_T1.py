# Andoni Olabarria Franco PL1
import psutil
import time
import signal
import sys
import requests
import urllib
import json

def handler(sig_num, frame): #SALBUESPEAN => Kanala itxi (Ctrl+C sakatu da)
 # Gertaera kudeatu
 print('\nSignal handler called with signal ' + str(sig_num))
 print('Check signal number on ' 'https://en.wikipedia.org/wiki/Signal_%28IPC%29#Default_action')
 kanala_hustu(gakoak)
 print('\nExiting gracefully')
 sys.exit(0)

def cpu_ram(gakoak): #CPU eta RAM portzentaiak lortzeko funtzioak
    while True:
        # KODEA: psutil liburutegia erabiliz, %CPU eta %RAM atera
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))
        balioak = [cpu, ram]
        datuak_kargatu(balioak, gakoak)
        time.sleep(15)


def kanala_sortu():
    metodoa = 'POST'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': 'Q8NYA4KNGPH5O39W',
              'name': 'Nire kanala',
              'field1': "%CPU",
              'field2': "%RAM"}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia_encoded,
                                 headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    edukiaJson = json.loads(edukia)
    Id = edukiaJson['id']
    api_key = edukiaJson["api_keys"][0]["api_key"]
    parametroak = [Id, api_key]
    #print(edukia)
    return parametroak

def datuak_kargatu(balioak, ids):
    metodoa = 'POST'
    uria = "https://api.thingspeak.com/update.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': ids[1],
              'name': 'Nire kanala',
              'field1': str(balioak[0]),
              'field2': str(balioak[1])}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia_encoded,
                                 headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    #edukia = erantzuna.content
    #print(edukia)

def kanala_hustu(gakoak):
    metodoa = 'DELETE'
    uria = "https://api.thingspeak.com/channels/" + str(gakoak[0]) + "/feeds.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': 'Q8NYA4KNGPH5O39W'}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia_encoded,
                                 headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    #edukia = erantzuna.content
    #print(edukia)


if __name__ == '__main__': #MAIN => Hastean kanala zabaldu eta datuak idatzi Ctrl+C sakaru arte
 # SIGINT jasotzen denean, "handler" metodoa exekutatuko da
 signal.signal(signal.SIGINT, handler)
 print('Running. Press CTRL-C to exit.')
 gakoak = kanala_sortu()
 print(gakoak)
 cpu_ram(gakoak)