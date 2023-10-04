import requests
from yc_company import Founder, Company
import openai, os
import google.generativeai as palm
import pdfplumber




palm_api_key = os.environ["PALM_API_KEY"]
palm.configure(api_key=palm_api_key)


instruction_prompt = "From the following founder bio and company description, write a personalized email to them writing about an interest in an internship. Less than 100 Words"
personal_details = "I, Alexander Aghili, am a sophomore at University of California, Santa Cruz majoring in computer science with experience in embedded systems, databases, and APIs."
structure_details = "" #Leave empty for now

def get_personal_details():
    with pdfplumber.open('../../Downloads/AlexanderAghili_Resume.pdf') as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    return "My resume is " + text


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
    prompt = instruction_prompt + "\n" + get_founder_prompt(company, founder) + "\n" + personal_details + "\n" + "Please be creative."
    
    completion = palm.generate_text(
        model="models/text-bison-001",
        prompt=prompt,
        temperature=1,
    )

    return completion.result

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


