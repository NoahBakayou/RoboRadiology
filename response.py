from openai import OpenAI
# from keys import API_TOKEN
from os import getenv
from dotenv import load_dotenv
load_dotenv()

API_TOKEN  = getenv('OPENAI_API_KEY')

#TODO: Get probability from model and issue.
# def model_feedback():
#   probablity = 0
#   issue = 'brain lesion'
#   return (probablity, issue)

def generate_response(organ_status, issue) -> str:
    organ_test = 'brain tumor xray'
    # organ_status, issue = model_feedback() 
    client = OpenAI(api_key = API_TOKEN)
    print(organ_status)
    user_content = f"Organ status = {organ_status}" 
    system_content = f"Please provide the result of your recent {organ_test}. Based on the organ_status, {organ_status} feedback, give consultation to the patient and explain what {issue} is."

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": system_content
        },
        {
          "role": "user",
          "content": user_content     }
      ],
      temperature=0.4,
      max_tokens=64,
      top_p=1
    )
   
    processed_response = response.choices[0].message.content
    return processed_response
if __name__ == '__main__':
    print(generate_response())