#!/bin/bash

import json
import os

print("name,website,ycdc_status,location")

dir_path = "./companies_json"
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
                
        print(csv)
    except Exception as e:
        pass