import csv
import datetime
import json
import os

import redis
import tweepy


def read_json(name, message=''):
    file = open(f'config/{name}.json', mode='r')
    data = json.load(file)
    file.close()
    print(f'reading {name} {message}')
    return data


def tweet(header, new_count, store_city, details=''):
    creds = read_json('creds', message='twitter')

    auth = tweepy.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
    auth.set_access_token(creds['access_token'], creds['access_token_secret'])

    api = tweepy.API(auth)

    body = f'{header}\n{new_count} available slots\n{details}'

    row = [store_city, new_count, datetime.datetime.now()]
    write_csv(row)

    if os.environ.get('DEBUG') != 1:
        api.update_status(body)


def write_csv(row):
    # name of csv file
    filename = "config/results.csv"
    headers = ['store', 'count', 'timestamp']

    file_exists = os.path.isfile(filename)

    # writing to csv file
    with open(filename, 'a') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the headers
        if not file_exists:
            csvwriter.writerow(headers)

        csvwriter.writerow(row)


def write_store(r_key, r_value, r_name="store_slots"):
    r = redis.Redis(
        host='redis',
        port=6379,
        password='',
        decode_responses=True)

    status = r.hset(r_name, r_key, r_value)
    print(f'write_store: {status}')


def read_store(r_key, r_name="store_slots"):
    r = redis.Redis(
        host='redis',
        port=6379,
        password='',
        decode_responses=True)

    data = int(r.get(r_name, r_key))
    print(f'read_store: {data}')
    return data
