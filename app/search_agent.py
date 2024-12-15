from langchain_community.tools.tavily_search import TavilySearchResults
from .config import TAVILY_API_KEY


def exec_search_agent(query: str) -> str:
    search = TavilySearchResults(api_key=TAVILY_API_KEY, max_results=2)
    search_results = search.invoke(query)

    tools = [search]

    return search_results
