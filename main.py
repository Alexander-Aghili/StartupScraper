#!/bin/python3

import json

f = open("yc-companies.json", "r")
data = json.load(f)
f.close()

for i in data['results'][0]['hits']:
    print(i['name'])
