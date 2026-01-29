import os
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()
client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversations: dict = {}  # this is "In-memory" implementation for trial; However, we will use database in production

@app.post("/chat")
# The following function takes 2 arguments:
# conversation_id: an identifier that our app uses to group messages that belong to the same chat session, so we can load the right message history and send it again on the next request.
# message: the actual message (prompt) to be sent to the model
async def chat(conversation_id: str, message: str, verbose: bool):
    # if it is a new chat session, create a new list in the dict, with its key: conversation_id
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    
    # Build message history
    # Assign the current chat session to a (history: list of dicts)
    history = conversations[conversation_id]
    history.append({"role": "user", "content": message})
    
    # Send to API with history
    response = client_openai.responses.create(
        model="gpt-4o-mini",
        input=history
    )
    
    assistant_message = response.output_text
    history.append({"role": "assistant", "content": assistant_message})

    if verbose == True:
        print(history)
    
    return {
        "response": assistant_message,
        "conversation_id": conversation_id,
        "turn": len(history) // 2 # since each “turn” is assumed to be one user + one assistant message, dividing the message count by 2 gives the turn number
    }
