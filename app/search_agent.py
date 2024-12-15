from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from .config import TAVILY_API_KEY, OPENAI_API_KEY
from langgraph.prebuilt import create_react_agent


def exec_search_agent(query: str) -> str:
    search = TavilySearchResults(api_key=TAVILY_API_KEY, max_results=2)
    tools = [search]

    model = ChatOpenAI(
        model="gpt-4o",
        openai_api_key=OPENAI_API_KEY,
    )
    agent_executor = create_react_agent(model, tools)

    response = agent_executor.invoke({"messages": [HumanMessage(content=query)]})

    # デバッグ出力を追加
    for i, msg in enumerate(response["messages"]):
        print(f"Message {i}: {msg.type} - {msg.content[:100]}...")

    return response["messages"][-1].content
