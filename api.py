from flask import Flask, jsonify, request, render_template
from email_creator import create_email_to_founder_palm
from yc_company import Company
import json
app = Flask(__name__)

@app.route('/genemail/<company_name>/<founder_name>')
def create_founder_email(company_name, founder_name):
    file_name = company_name.replace("%20", " ") + ".json"
    file_path = "./companies_json/" + file_name
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        company = Company(data['slug'])
        #company.short_desc = None due to how create_company_from_json wroks
        company.create_company_from_json(data) 
        for founder in company.founders:
            if founder.full_name == founder_name:
                response = create_email_to_founder_palm(company, founder)
                return render_template('email.html', email_response=response)


if __name__ == '__main__':
    app.run(debug = True)