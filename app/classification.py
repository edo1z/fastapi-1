from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .config import OPENAI_API_KEY


async def get_classification(text: str) -> str:
    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=OPENAI_API_KEY,
        temperature=0
    )

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """
        あなたはテキスト分類の専門家です。
        入力されたテキストを以下のカテゴリのいずれかに分類してください：

        - 質問：疑問符や「〜ですか？」「〜かな？」などの疑問形、または情報を求める文
        - 要望：「〜してほしい」「〜お願いします」などの依頼や要求
        - 苦情：不満、クレーム、否定的な意見
        - その他：上記に当てはまらないもの

        カテゴリ名のみを返してください。
        """),
        ("user", "{text}")
    ])

    prompt = prompt_template.invoke({"text": text})
    response = await model.ainvoke(prompt)

    return response.content