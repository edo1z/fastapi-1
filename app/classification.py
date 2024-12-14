from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from .config import OPENAI_API_KEY


class TextClassification(BaseModel):
    category: str = Field(
        enum=["質問", "要望", "苦情", "その他"],
        description="テキストのカテゴリ分類"
    )
    sentiment: str = Field(
        enum=["ポジティブ", "ネガティブ", "ニュートラル"],
        description="テキストの感情分析"
    )
    aggressiveness: int = Field(
        ge=1, le=10,
        description="テキストの攻撃性（1-10のスケール）"
    )
    language: str = Field(
        enum=["日本語", "英語", "中国語", "韓国語", "その他"],
        description="テキストの使用言語"
    )


async def get_classification(text: str) -> TextClassification:
    model = ChatOpenAI(
        model="gpt-4o",
        openai_api_key=OPENAI_API_KEY,
        temperature=0
    ).with_structured_output(TextClassification)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        テキストから以下の情報を抽出してください：
        - カテゴリ
        - 感情
        - 攻撃性
        - 使用言語

        指定された形式で返してください。
        """),
        ("user", "{text}")
    ]).invoke({"text": text})

    return await model.ainvoke(prompt)