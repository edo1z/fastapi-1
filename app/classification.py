from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from .config import OPENAI_API_KEY


class TextClassification(BaseModel):
    category: str = Field(description="質問・要望・苦情・その他のいずれか")
    sentiment: str = Field(description="テキストの感情（ポジティブ・ネガティブ・ニュートラル）")
    aggressiveness: int = Field(description="テキストの攻撃性（1-10のスケール）")
    language: str = Field(description="テキストの使用言語")


async def get_classification(text: str) -> TextClassification:
    model = ChatOpenAI(
        model="gpt-4o",
        openai_api_key=OPENAI_API_KEY,
        temperature=0
    ).with_structured_output(TextClassification)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """
        テキストを分析し、以下の情報を抽出してください：
        - カテゴリ（質問・要望・苦情・その他）
        - 感情（ポジティブ・ネガティブ・ニュートラル）
        - 攻撃性（1-10のスケール）
        - 使用言語

        指定された形式で結果を返してください。
        """),
        ("user", "{text}")
    ])

    prompt = prompt_template.invoke({"text": text})
    response = await model.ainvoke(prompt)

    return response