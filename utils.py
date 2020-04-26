import json


def read_json(name):
    file = open(f'{name}.json', mode='r')
    data = json.load(file)
    file.close()
    print(f'reading {name}')
    return data