from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select
from . import models
from . import chat
from . import search
from pydantic import BaseModel
from . import classification
from . import extraction
from . import chatbot
from . import search_agent


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class ChatbotRequest(BaseModel):
    message: str
    thread_id: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/users/", response_model=models.User)
def create_user(user: models.UserCreate, db: Session = Depends(models.get_db)):
    existing_user = db.exec(
        select(models.User).where(models.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="このメールアドレスは既に登録されています"
        )

    db_user = models.User.model_validate(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=list[models.User])
def read_users(db: Session = Depends(models.get_db)):
    return db.exec(select(models.User)).all()


@app.post("/chat")
async def create_chat(chat_request: ChatRequest):
    return StreamingResponse(
        chat.get_chat_stream(chat_request.message), media_type="text/event-stream"
    )


@app.get("/search")
async def search_pages():
    return await search.count_pages()


@app.post("/classify")
async def classify_text(text: str):
    result = await classification.get_classification(text)
    return result


@app.post("/extract")
async def extract_info(text: str):
    result = await extraction.get_extraction(text)
    return result


@app.post("/chatbot")
async def create_chatbot_response(request: ChatbotRequest):
    response = await chatbot.chatbot_response(request.message, request.thread_id)
    return {"response": response}


@app.post("/search-agent")
async def search_with_agent(query: str):
    result = search_agent.exec_search_agent(query)
    return {"results": result}
