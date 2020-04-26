import csv
import datetime
import json
import os

import tweepy


def read_json(name, message=''):
    file = open(f'config/{name}.json', mode='r')
    data = json.load(file)
    file.close()
    print(f'reading {name} {message}')
    return data


def tweet(header, count, store_city, details=''):
    creds = read_json('creds', message='twitter')

    auth = tweepy.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
    auth.set_access_token(creds['access_token'], creds['access_token_secret'])

    api = tweepy.API(auth)

    body = f'{header}\n{count} available slots\n{details}'

    row = [store_city, count, datetime.datetime.now()]
    write_csv(row)
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