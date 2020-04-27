import csv

import requests
import time
import datetime
import tweepy

from bs4 import BeautifulSoup

from utils import read_json, tweet

import authy

payload = "ControllerName=ReserveTimeslot&FulfillmentType=Pickup"

headers = authy.authenticate()

index = {}
counter = 0

while 1:
    print(f'[attempt: {counter}] {datetime.datetime.now()}')
    store_list = read_json('stores')
    # store_list = {'drexel': '1AD0123688'}
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

                if store_name is not None:
                    store_name = store_name.get_text()
                    store_city = store_city.get_text()
                    store_region = store_region.get_text()
                else:
                    # reauth if empty
                    headers = authy.authenticate()
                    break

                num_slots = 0
                for div in soup.find_all('div', class_='timeslotPicker__timeslotButton--wrap timeslotPicker__cell'):
                    details = str.strip(div.get_text())
                    if details != 'Sold Out':
                        header = f'[{store_name}, {store_city}, {store_region}]'
                        slot_id = f'{header}_{details}'
                        if store_name not in index:
                            index.setdefault(store_name, [])
                        if details not in index[store_name]:
                            num_slots += 1
                            index[store_name].append(details)
                            print(f'TimeSlot Available: {details}')

                # tweet or clean up
                if num_slots == 1:
                    # get the most recently added slot
                    details = index[store_name][-1]
                    tweet(header, num_slots, store_city, details)
                elif num_slots > 1:
                    tweet(header, num_slots, store_city)
                    print('')
                else:
                    index[store_name] = []
            else:
                # if non-200 re-authenticate
                print(f'Error: {res.status_code} response. Trying to re-authenticate')
                headers = authy.authenticate()
        except Exception as e:
            print(f'Error on request: {e}')

    timeout = 180

    print(f'sleep {timeout}')
    counter += 1
    time.sleep(timeout)
