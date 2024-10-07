from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from logic import start_chat, process_chat

app = FastAPI()

class Chat(BaseModel):
    query: str

chat_history = []

@app.post("/chat")
async def api_process_chat(chat: Chat):
    global chat_history
    try:
        start_chat()
        answer, chat_history = process_chat(chat.query, chat_history)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the query: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to the Sukwo customer care center!, how can I help you?"}

if __name__ == "__main__":
    start_chat()