from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select
from . import models
from . import chat
from . import search
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


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
def search_pages():
    return search.count_pages()
