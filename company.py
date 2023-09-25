import requests
import html
import re
import json
import time

def get_html(link):
    res = requests.get(link)
    return html.unescape(res.text)

def get_json_from_html(html):
    regex_pattern = r"<script type=\"application/json\" class=\"js-react-on-rails-component\" data-component-name=\"CompaniesShowPage\" data-dom-id=\"CompaniesShowPage-react-component-[a-zA-Z0-9-]+\">\n?(.*)\n?</script>"
    match = re.search(regex_pattern, html, re.DOTALL)
    if match:
        return json.loads(match.group(1))
        
        
class Company:
    yc_link = ""

    name = ""
    slug = ""
    website = ""
    linkedin = ""
    ycdc_status = ""
    team_size = 0
    location = ""
    short_desc = ""
    founders = []
    def __init__(self, slug):
        self.slug = slug
        self.yc_link = "https://www.ycombinator.com/companies/" + slug
        self.founders = []
        self.populate_company()

    def populate_company(self):
        html = get_html(self.yc_link)
        json = get_json_from_html(html)
        company = json['company']

        self.name = company.get('name')
        self.website = company.get('website')
        self.linkedin = company.get('linkedin_url')
        self.ycdc_status = company.get('ycdc_status')
        self.team_size = company.get('team_size')
        self.location = company.get('location')
        self.short_desc = company.get('one_liner') #Change to long_desciption?
        for founder in company.get('founders'):
            self.founders.append(
                Founder(founder.get('is_active'), founder.get('founder_bio'),
                        founder.get('full_name'), founder.get('title'),
                        founder.get('linkedin_url'))
            )
        print(self.name)
        print(self.founders[0].full_name)
        time.sleep(1)
    
    def get_json(self):
        company_map = {'name': self.name, 'slug': self.slug, 'website': self.website,
                       'linkedin': self.linkedin, 'ycdc_status': self.ycdc_status, 'team_size': self.team_size,
                       'location': self.location, 'short_desc': self.short_desc}
        for founder in self.founders:
            company_map['founders'] = company_map.get('founders', [])
            company_map['founders'].append(founder.get_map())
        return json.dumps(company_map, indent=4)

class Founder:
    is_active = ""
    bio = ""
    full_name = ""
    title = ""
    linkedin_url = ""

    def __init__(self, is_active, bio, full_name, title, linkedin):
        self.is_active = is_active
        self.bio = bio
        self.full_name = full_name
        self.title = title
        self.linkedin_url = linkedin

    def get_map(self):
        return {
            'full_name': self.full_name,
            'title': self.title,
            'is_active': self.is_active,
            'bio': self.bio,
            'linkedin': self.linkedin_url
        }
    