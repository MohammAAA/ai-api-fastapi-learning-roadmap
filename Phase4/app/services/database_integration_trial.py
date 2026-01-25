from sqlalchemy.ext.declarative import declarative_base # The parent class of the ORM (Object-relational mapping) models
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import Session, sessionmaker
from datetime import datetime,timezone
from fastapi import FastAPI, HTTPException, Depends
from openai import OpenAI
import json
import os


Base = declarative_base() # Create a class instance of the ORM base class called (Base)
app = FastAPI()
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# we will use SQLite for learning, and PostgreSQL for production
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL) # The Engine's role is to connect our Python code to the real database. We specify the database type (e.g.: SQLite) and the sqlalchemy handles all the SQL work

SessionLocal = sessionmaker(bind=engine)

def get_db():
    return SessionLocal()

class Conversation(Base): # This class is inherited from the parent ORM class
    __tablename__ = "conversations"
    id = Column(String, primary_key=True)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    messages = Column(String)  # Type is string as it will be stored as (JSON string serialized)

Base.metadata.create_all(engine)  # Creates the table, the data class (Conversation) is saved in the Base's metadata at the (Conversation) class instantiation

# Now store persistent conversations
@app.post("/chat")
def chat(conversation_id: str, message: str, db: Session = Depends(get_db)):
    user_message = [{"role": "user",
                    "message": message}] # I want to treat json_message as a list of dicts so that I can append it to another list (i.e.: the conversation list)
    json_message_serialized = json.dumps([user_message]) # serialize the python object to JSON string
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    log_message = f"Conversation {conversation_id} has been just loaded"
    if not conv:
        # conversation ID is not found in the database. Add this new conversation to the database
        conv = Conversation(id=conversation_id, user_id="user1", messages=json_message_serialized)
        db.add(conv)
        db.commit()
        # We will perform a refresh to get a conv.id that we will need in the output
        db.refresh(conv)
        log_message = f"Conversation {conversation_id} has been just created" # overwriting the log message to indicate createion, not loading
    # Convert the db stored conversation messages to a python object (i.e.: list of dicts)
    stored_messages = json.loads(conv.messages) # This will return either dict or list
    # We need to make sure the (stored_messages) is a list (not dict) so we can append() to it
    if isinstance(stored_messages, dict):
        stored_messages = [stored_messages]  # cast old -dict- format to list
    # Append the dict "json_message" to the list of dicts "stored_messages"
    stored_messages.append(user_message)
    # Convert the list of dicts "stored_messages" to a serialized JSON string in order to pass it to the AI model
    json_stored_messages = json.dumps(stored_messages)
    gpt_response = client_openai.responses.create(
        model="gpt-4o-mini",
        input=json_stored_messages,
        temperature=1.0,
    )
    # construct the AI reponse structure as dict 
    ai_response = {"role": "assistant",
                     "message": gpt_response.output_text}
    # append the AI response to the list of the conversation dicts
    stored_messages.append(ai_response)
    # Convert the list of dicts "stored_messages" to a serialized JSON string in order to save it again to the database
    json_stored_messages = json.dumps(stored_messages)
    # commit the conversation to be saved to the database
    conv.messages = json_stored_messages
    db.add(conv)    
    db.commit()

    # structure the output that will be returned to the user
    output = {
        "INFO": log_message,
        "user_id": conv.user_id,
        "conversation_id": conv.id,
        "conversation_created_at": conv.created_at,
        "conversation_history": conv.messages,
        "response": gpt_response.output_text
    }
    # output = json.dumps(output) This line will fail ("TypeError: Object of type datetime is not JSON serializable")
    # A simple fix is to just return the output as is and fastAPI will serialize it for us (it uses encoder utilities (ex.: jsonable_encoder) that helps converting non-JSON-compatible objects to JSON-compatible data) 
    return output

