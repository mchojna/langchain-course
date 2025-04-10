from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str) -> str:
    """Search for LinkedIn or Twitter profile page URL"""
    search = TavilySearchResults()
    result = search.run(f"{name}")
    return result
