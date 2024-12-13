from datetime import datetime, UTC
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session
from pydantic import EmailStr
from .config import DATABASE_URL

# データベース設定
engine = create_engine(DATABASE_URL)


# モデル定義（schemas.pyとmodels.pyが統合される）
class UserBase(SQLModel):
    name: str = Field(
        min_length=1,
        max_length=50,
        description="ユーザー名は1-50文字で入力してください"
    )
    email: EmailStr = Field(
        unique=True,
        index=True,
        description="有効なメールアドレスを入力してください"
    )


class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)},
    )


class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=100,
        description="パスワードは8文字以上で入力してください"
    )


# DBセッション依存性
def get_db():
    with Session(engine) as session:
        yield session


# アプリ起動時にテーブルを作成
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
