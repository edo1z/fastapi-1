from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from .config import OPENAI_API_KEY
from typing import AsyncGenerator


# チャットボットの初期化
model = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY,
    streaming=True
)

# グラフの設定
workflow = StateGraph(state_schema=MessagesState)

def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}

workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# メモリの設定
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

async def chatbot_response(message: str, thread_id: str) -> AsyncGenerator[str, None]:
    print(f"Debug - Message: {message}, Thread ID: {thread_id}")  # デバッグ用
    config = {"configurable": {"thread_id": thread_id}}
    input_messages = [HumanMessage(message)]

    response = app.invoke({"messages": input_messages}, config)
    print(f"Debug - Response: {response}")  # デバッグ用
    yield response["messages"][-1].content
