from yc_company import Founder, Company
import openai, os

openai.organization = "org-LTjW6EI8VHhOhFqFmbekYv0X"
openai.api_key = os.getenv("OPENAI_API_KEY")

instruction_prompt = "From the following founder bio and company description, write a personalized email to them writing about an interest in an internship. Less than 100 Words"
personal_details = "I, Alexander Aghili, am a sophomore at University of California, Santa Cruz with experience in embedded systems, databases, and APIs."
structure_details = "" #Leave empty for now
def get_founder_prompt(company: Company, founder: Founder):
    return founder.full_name + " is the " + founder.title + " of " + company.name + ". The bio is: " + founder.bio

def create_email_to_founder(company: Company, founder: Founder):
    context_messages = []
    context_messages.append({'role': 'system', 'content': instruction_prompt})
    context_messages.append({'role': 'system', 'content': get_founder_prompt(company,founder)})
    context_messages.append({'role': 'system', 'content': personal_details})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                        messages=context_messages)
    
    return str(chat.choices[0].message.content)
