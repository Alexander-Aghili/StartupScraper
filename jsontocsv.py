#!/bin/bash

import json
import os

print("name,website,ycdc_status,location")

dir_path = "./companies_json"
domain_link="http://localhost:5000/"
gen_email_link= domain_link + "genemail/"
dir = os.listdir(dir_path)

for file in dir:
    file_path = os.path.join(dir_path, file)

    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            csv = "\"" + data["name"] + "\"," + data["website"] + "," 
            csv = csv + data["ycdc_status"] + ",\"" + data["location"] + "\""
            for founder in data["founders"]:
                csv = csv + ",\"" + founder["full_name"] + "\""
                if founder["title"] is None:
                    founder["title"] = ""
                csv = csv + ",\"" + founder["title"] + "\""
                
                founder_name_link = founder["full_name"].replace(" ", "%20")
                company_name_link = data["name"].replace(" ", "%20")
                csv = csv + ",\"" + gen_email_link + company_name_link + "/" + founder_name_link + "\""

        print(csv)
    except Exception as e:
        pass