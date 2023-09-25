#!/bin/python3

from email_creator import create_email_to_founder
from company import Company
import json

f = open("yc-companies.json", "r")
data = json.load(f)
f.close()

for company in data['results'][0]['hits']:
    c = Company(company["slug"])
    f = open("./companies_json/" + c.name + ".json", "w+")
    f.write(c.get_json())
    f.close()
    