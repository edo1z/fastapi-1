from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from . import models

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
    db_user = models.User.model_validate(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=list[models.User])
def read_users(db: Session = Depends(models.get_db)):
    return db.exec(select(models.User)).all()
