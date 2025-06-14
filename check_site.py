from time import sleep
import requests
from bs4 import BeautifulSoup
import os

URL = os.environ['URL']
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

def check_element():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find('a', href='https://maratonaclubedeportugal.com/wp-content/uploads/Announcement_04.06.pdf',
                            string='Registrations soon')
        return element is not None
    except Exception as e:
        print(f'Error checking site: {e}')
        return False

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f'Failed to send message: {response.text}')
    else:
        print('Notification sent.')

retries = 0
backoff = [5, 10, 20, 40, 80, 160, 240]
while(not check_element() and retries < len(backoff)):
    print(f"Could not find element, retrying in {backoff[retries]} seconds")
    sleep(backoff[retries])
    retries+=1

if(retries == (len(backoff)-1)):
        alert_msg = f'⚠️Anmälan kan ha öppnat! Hemsidan har i alla fall ändrats: {URL}'
        send_telegram_message(alert_msg)
else:
    print("Element found. All good.")
