import requests
from yc_company import Founder, Company
import openai, os
import google.generativeai as palm


palm.configure(api_key='AIzaSyBOp21--YO2qrkFnQJ4ySJRDL4bk5nXJ8w')


instruction_prompt = "From the following founder bio and company description, write a personalized email to them writing about an interest in an internship. Less than 100 Words"
personal_details = "I, Alexander Aghili, am a sophomore at University of California, Santa Cruz with experience in embedded systems, databases, and APIs."
structure_details = "" #Leave empty for now
def get_founder_prompt(company: Company, founder: Founder):
    if founder.bio is None:
        founder.bio = ""
    if founder.title is None:
        founder.title = ""
    return founder.full_name + " is the " + founder.title + " of " + company.name + ". The bio is: " + founder.bio


def get_email_format():
    return """Please use the following format: 
        Dear Mr. [Founder Last Name],
        [Talk about my interest in the company and their mission]
        [Talk about my experience]
        [Reiterate my interest]
        Sincerely,
        Alexander Aghili
    """ 

def create_email_to_founder_palm(company: Company, founder: Founder):
    message = instruction_prompt + "\n" + get_founder_prompt(company, founder) + "\n" + personal_details + "\n" + get_email_format()
    return palm.chat(messages=message).last

def create_email_to_founder_gpt(company: Company, founder: Founder):
    openai.organization = "org-LTjW6EI8VHhOhFqFmbekYv0X"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    context_messages = []
    context_messages.append({'role': 'system', 'content': instruction_prompt})
    context_messages.append({'role': 'system', 'content': get_founder_prompt(company,founder)})
    context_messages.append({'role': 'system', 'content': personal_details})
    context_messages.append({'role': 'system', 'content': get_email_format()})
    
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                        messages=context_messages)
    
    return str(chat.choices[0].message.content)


