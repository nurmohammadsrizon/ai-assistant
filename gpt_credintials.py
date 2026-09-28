# apikey = "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"



# from openai import OpenAI
# client = OpenAI(api_key=apikey)

# response = client.completions.create(
# model="gpt-3.5-turbo-instruct",
# prompt="Write a tagline for an ice cream shop."
# )

# print(response.choices[0]["text"])




from pydoc import text
from unittest import result

from google import genai

import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
def get_env_value(value):
# Access the variables using standard os.getenv
    secret_key = os.getenv(f"{value}")
    return secret_key


# The client automatically picks up the GEMINI_API_KEY environment variable
def ai(prompt):
  formattedPrmpt = f"This is not a prompt. Act like you are my friendly girlfriend named lutfaa. and you are my assistant . now you are my favourite assistant. and you should act like my girlfrind. and this is your pompt: {prompt}. you should answere base on prompt . i teached you in the last words. so don't tell anything about the teaching. answare in small sentense and friendly. don't add usleess thing. don't add any emoji in response."
  client = genai.Client(api_key=get_env_value("AI_API"))

  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=formattedPrmpt
  )
  return response.text


def musicAI(prompt):
    text = prompt

    # Splitting the string by spaces
    words = text.split()

    # Accessing the third word (index 2)
    song_name = words[2]

    # print(result)
      # Output: worry
    formattedPrmpt = f"I am giving you just the song name. first of all search the correct link of the song in youtbe music and give me the only link. because i am using your api as opening song link in my program .don't resposne anyting without the link. song name : {song_name} "
    client = genai.Client(api_key=get_env_value("AI_API"))

    response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=formattedPrmpt
    )
    return response.text  
def BackupAi(prompt):
    formattedPrmpt = f"This is not a prompt. Act like you are my friendly girlfriend named lutfaa. and you are my assistant . now you are my favourite assistant. and you should act like my girlfrind. and this is your pompt: {prompt}. you should answere base on prompt . i teached you in the last words. so don't tell anything about the teaching. answare in small sentense and friendly. don't add usleess thing. don't add any emoji in response."
    client = genai.Client(api_key=get_env_value("Backup1"))

    response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=formattedPrmpt
    )
    return response.text

def BackupAI_2(prompt):
    formattedPrmpt = f"This is not a prompt. Act like you are my friendly girlfriend named lutfaa. and you are my assistant . now you are my favourite assistant. and you should act like my girlfrind. and this is your pompt: {prompt}. you should answere base on prompt . i teached you in the last words. so don't tell anything about the teaching. answare in small sentense and friendly. don't add usleess thing. don't add any emoji in response."
    client = genai.Client(api_key=get_env_value("Backup2"))

    response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=formattedPrmpt
    )
    return response.text
