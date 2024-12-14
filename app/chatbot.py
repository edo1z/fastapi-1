from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .config import OPENAI_API_KEY

# チャットボットの初期化
model = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY,
)

# プロンプトテンプレートの設定
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "あなたは親切で丁寧な日本語アシスタントです。"
            "ユーザーの質問に対して、簡潔かつ分かりやすく回答してください。"
            "毎回回答に絵文字を追加してください。",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# グラフの設定
workflow = StateGraph(state_schema=MessagesState)


async def call_model(state: MessagesState):
    prompt = prompt_template.invoke(state)
    response = await model.ainvoke(prompt)
    return {"messages": response}


workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# メモリの設定
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


async def chatbot_response(message: str, thread_id: str) -> str:
    config = {"configurable": {"thread_id": thread_id}}
    input_messages = [HumanMessage(message)]
    response = await app.ainvoke({"messages": input_messages}, config)
    return response["messages"][-1].content
