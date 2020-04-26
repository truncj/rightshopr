import requests
import time
import datetime
import tweepy

from bs4 import BeautifulSoup

from utils import read_json
import authy

creds = read_json('creds', message='twitter')

auth = tweepy.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
auth.set_access_token(creds['access_token'], creds['access_token_secret'])

api = tweepy.API(auth)

payload = "ControllerName=ReserveTimeslot&FulfillmentType=Pickup"

headers = authy.authenticate()

index = []

# test store
# store_list = { 'drexel': '1AD0123688'}

counter = 0

while 1:
    print(f'[attempt: {counter}] {datetime.datetime.now()}')
    store_list = read_json('stores')
    for store_name in store_list:
        try:
            store_id = store_list[store_name]

            url = f'https://shop.shoprite.com/store/{store_id}/reserve-timeslot-process'
            res = requests.request("POST", url, data=payload, headers=headers)

            if res.status_code == 200:
                data = res.text

                print(f'{store_name} response: {res.status_code}')

                soup = BeautifulSoup(data, 'html.parser')

                store_name = soup.find('span', class_='contactInfo--title')
                store_city = soup.find('span', class_='address__city')
                store_region = soup.find('span', class_='address__region')

                if store_name != None:
                    store_name = store_name.get_text()
                    store_city = store_city.get_text()
                    store_region = store_region.get_text()
                else:
                    # reauth if empty
                    headers = authy.authenticate()
                    break

                num_slots = 0
                for div in soup.find_all('div', class_='timeslotPicker__timeslotButton--wrap timeslotPicker__cell'):
                    text = str.strip(div.get_text())
                    if text != 'Sold Out':
                        header = f'[{store_name}, {store_city}, {store_region}]'
                        body = f'[{header}]\n{text}'
                        slot_id = header + text
                        if slot_id not in index:
                            num_slots += 1
                            index.append(slot_id)
                            print(f'TimeSlot Available: {text}')

                if num_slots == 1:
                    api.update_status(body)
                elif num_slots > 1:
                    api.update_status(f'[{header}]\n{num_slots} available slots')
                else:
                    # clear out index for that store when no slots are found
                    for slot_id in index:
                        if slot_id.startswith(store_name):
                            index.remove(slot_id)
            else:
                # if non-200 re-authenticate
                headers = authy.authenticate()
        except Exception as e:
            print(f'Error on request: {e}')

    timeout = 180

    print(f'sleep {timeout}')
    counter += 1
    time.sleep(timeout)
