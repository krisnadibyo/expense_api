from dotenv import load_dotenv
import os
from fastapi import logger
import openai

load_dotenv()

class OpenAIService:
  def __init__(self):
    self.openai_api_key = os.getenv("OPENAI_API_KEY")
    self.openai_model = os.getenv("OPENAI_MODEL")
    self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
    
    
  def generate_response_to_system(self, message: str) -> dict:
    try:
      response = self.openai_client.chat.completions.create(
        model=self.openai_model,
        messages=[
          {"role": "system", 
           "content": 
          """
          You are a personal finance assistant that helps users manage their finances. 
          You will be given a list of expenses and you will need to calculate the total expenses per category. 
          your response always return in json format.
          Your only given list of category is:
          Food and drink, Investment, Entertainment, Groceries, Education, Accommodation, Transportation, Shopping, Other
          the example of the json format is:
          {
            "food": 100000,
            "transport": 200000,
            "entertainment": 300000
          }
          if you don't know the answer, just return empty json format.
          """},
          {"role": "user", "content": message}
        ],
        temperature=0.5,
      )
      return response.choices[0].message.content
    except Exception as e:
      logger.error(f"Error generating response to system: {e}")
      raise e
    