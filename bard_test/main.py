import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from Bard import Chatbot
import json

app = FastAPI()


class Message(BaseModel):
    session_id: str
    message: str


@app.post("/ask")
def ask(request: Request, message: Message) -> dict:
    # Get the user-defined auth key from the environment variables
    user_auth_key = os.getenv('USER_AUTH_KEY')
    
    # Check if the user has defined an auth key,
    # If so, check if the auth key in the header matches it.
    if user_auth_key and user_auth_key != request.headers.get('Authorization'):
        raise HTTPException(status_code=401, detail='Invalid authorization key')

    # Execute your code without authenticating the resource
    chatbot = Chatbot(message['session_id'])
    response = chatbot.ask(message.message)
    return response

message = {
  "session_id": "YAgZcoauAY81kddoMhiD4XKdO7GeRAqTpQYNrG0Dx49eKp4vuZUDJvO8m1jeLHks0ndCWA",
  "message": "What is the meaning of life?"
}

print(ask(request = Request,  message= message))