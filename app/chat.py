from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .config import OPENAI_API_KEY
from typing import AsyncGenerator


async def get_chat_stream(user_message: str) -> AsyncGenerator[str, None]:
    model = ChatOpenAI(
        model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, streaming=True
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "Translate the following from {source_lang} into {target_lang}"),
            ("user", "{text}"),
        ]
    )

    prompt = prompt_template.invoke(
        {"source_lang": "Japanese", "target_lang": "English", "text": user_message}
    )

    async for chunk in model.astream(prompt):
        if chunk.content:
            yield chunk.content
