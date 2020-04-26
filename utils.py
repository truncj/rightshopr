import json


def read_json(name, message=''):
    file = open(f'config/{name}.json', mode='r')
    data = json.load(file)
    file.close()
    print(f'reading {name} {message}')
    return data