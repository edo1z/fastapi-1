from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from .config import OPENAI_API_KEY


def get_chat_response(user_message: str) -> str:
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

    messages = [
        SystemMessage(content="Translate the following from Japanese into English"),
        HumanMessage(content=user_message),
    ]

    response = model.invoke(messages)
    return response.content
