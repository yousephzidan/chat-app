from controllers import chat_bp
from models import Messages, Users
from flask import session

@chat_bp.post("/chat/<contact_id:int>")
def chat(contact_id):
    ...



