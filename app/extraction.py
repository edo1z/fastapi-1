from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from .config import OPENAI_API_KEY


class Person(BaseModel):
    """Information about a person."""

    name: Optional[str] = Field(default=None, description="The name of the person")
    hair_color: Optional[str] = Field(
        default=None, description="The color of the person's hair if known"
    )
    height_in_meters: Optional[str] = Field(
        default=None, description="Height measured in meters"
    )


class People(BaseModel):
    data: list[Person] = Field(default=[], description="List of person")


async def get_extraction(text: str) -> People:
    model = ChatOpenAI(
        model="gpt-4o", openai_api_key=OPENAI_API_KEY, temperature=0
    ).with_structured_output(People)

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "あなたは専門的な情報抽出アルゴリズムです。"
                "テキストから関連情報のみを抽出してください。"
                "抽出を求められた属性の値が不明な場合は、"
                "その属性の値としてnullを返してください。",
            ),
            ("human", "{text}"),
        ]
    )

    prompt = prompt_template.invoke({"text": text})
    return await model.ainvoke(prompt)
