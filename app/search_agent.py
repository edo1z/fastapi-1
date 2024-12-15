from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from .config import TAVILY_API_KEY, OPENAI_API_KEY


def exec_search_agent(query: str) -> str:
    search = TavilySearchResults(api_key=TAVILY_API_KEY, max_results=2)
    tools = [search]

    model = ChatOpenAI(
        model="gpt-4o",
        openai_api_key=OPENAI_API_KEY,
    )
    model_with_tools = model.bind_tools(tools)

    response = model_with_tools.invoke([HumanMessage(content=query)])

    print(f"ContentString: {response.content}")
    print(f"ToolCalls: {response.tool_calls}")

    return response.tool_calls
