import os
from dotenv import load_dotenv
from fastapi import HTTPException, logger
import httpx

from app.services.openai_service import OpenAIService


load_dotenv()

ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID=os.getenv("PHONE_NUMBER_ID")
VERSION=os.getenv("VERSION")
VERIFY_TOKEN=os.getenv("VERIFY_TOKEN")

class WaService:
  def __init__(self, openai_service: OpenAIService):
    self.access_token = ACCESS_TOKEN
    self.phone_number_id = PHONE_NUMBER_ID
    self.version = VERSION
    self.verify_token = VERIFY_TOKEN
    self.openai_service = openai_service

  async def verify_webhook(
    self,
    mode: str,
    challenge: str,
    verify_token: str
  ):
    # Verify the webhook
    if mode == "subscribe" and verify_token == self.verify_token:
      return int(challenge)
    
    raise HTTPException(
      status_code=403,
      detail="Verification failed"
    )
    
  async def handle_message(self, message: dict):
    """
    Handle incoming WhatsApp message webhook
    
    Args:
        message (dict): The message payload from WhatsApp webhook
        
    Returns:
        dict: Response with status and message details
    """
    try:
      if message.get("object") != "whatsapp_business_account":
        return {"status": "error", "message": "not a valid webhook object"}
      # Check if the message contains valid entries
      if not message.get("entry"):
        return {"status": "error", "message": "No entry in the webhook payload"}
    
    # Process only messages from users, not system messages
      for entry in message["entry"]:
        for change in entry.get("changes", []):
          value = change.get("value", {})
          
          # Check for messages in the payload
          if not value.get("messages"):
            continue
            
          for msg in value["messages"]:
            # Filter out system messages, only process user messages
            if msg.get("type") == "text" and "from" in msg:
              # Extract the message text and sender information
              message_body = msg["text"]["body"]
              sender_id = msg["from"]
              
              # TODO: Process the message
              response = self.openai_service.generate_response_to_system(message_body)
              await self.send_message(response, sender_id)
              
          return {
            "status": "success",
            "message": "message received",
            "timestamp": msg.get("timestamp", "")
          }
      
      # If we get here, no valid user messages were found
      return {"status": "ignored", "message": "No user messages in the payload"}
      
    except Exception as e:
      return {"status": "error", "message": str(e)}
    
  async def send_message(self, message: str, recipient_waid: str):
    url = f"https://graph.facebook.com/{self.version}/{self.phone_number_id}/messages"
    headers = {
      "Authorization": f"Bearer {self.access_token}",
      "Content-Type": "application/json"
    }
    data = {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": recipient_waid,
      "type": "text",
      "text": {
        "body": message
      }
    }
    async with httpx.AsyncClient() as client:
      response = await client.post(url, headers=headers, json=data)
      if response.status_code == 200:
        logger.logger.info(f"Message sent successfully to {recipient_waid}: {message}")
      else:
        logger.logger.info(f"Failed to send message: {response}")
