from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from .config import OPENAI_API_KEY
from typing import AsyncGenerator


async def get_chat_stream(user_message: str) -> AsyncGenerator[str, None]:
    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=OPENAI_API_KEY,
        streaming=True
    )

    messages = [
        SystemMessage(content="日本語から英語に翻訳してください。"),
        HumanMessage(content=user_message),
    ]

    async for chunk in model.astream(messages):
        if chunk.content:
            yield chunk.content
