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

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) # This is a class that is acting like a callable factory function. Instead of calling Session(engine=my_engine, autoflush=False, autocommit=False) directly with all the config, we configure sessionmaker once, then call it repeatedly.

# The following is a test code for debugging the (yield), the code works, however if an exception occurs the yield will not return to its last stack pointer so the db.close() will not be executed. So it is better to be in (finally:)
# def get_db():
#     db = SessionLocal()
#     try:
#         print("LOG: will yield the db now")
#         yield db
#         print("LOG: resuming get_db()")
#         db.close()
#         print("LOG: db session closed")

#     except NameError as e:
#         pass


def get_db():
    db = SessionLocal()
    try:
        print("LOG: will yield the db now")
        yield db
        print("LOG: resuming get_db()")
    finally: # The following code block will be executed either after the function (chat()) returns, an exception occurs in chat(), or just after the function get_db() itself returns (e.g.: if we use "return db" instead of "yield db" ... however, never do this logical mistake)
        db.close()
        print("LOG: db session closed")

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
    print("LOG: entered the /chat endpoint")
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
    # db.add(conv) # This is optional, as (conv) came from a query; it’s already in the session so no need for adding   
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
    print("LOG: returning to get_db()")
    # output = json.dumps(output) This line will fail ("TypeError: Object of type datetime is not JSON serializable")
    # A simple fix is to just return the output as is and fastAPI will serialize it for us (it uses encoder utilities (ex.: jsonable_encoder) that helps converting non-JSON-compatible objects to JSON-compatible data) 
    return output

