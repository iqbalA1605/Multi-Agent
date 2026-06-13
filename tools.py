from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os 
from rich import print
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
@tool
def web_search(query : str) -> str:
    """
Search the web for accurate and recent information on a user-provided topic.

This tool should be used by research agents to gather external knowledge,
current events, statistics, articles, and factual information from trusted sources.

Returns:
- Search result titles
- Source URLs
- Relevant content snippets

Best used when performing research, fact-finding, or collecting supporting evidence.
"""
    results = tavily.search(query=query, max=4)
    
    if not results or 'results' not in results:
        return "No search results found for this query."
    
    out = []
    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    return "\n----\n".join(out)
@tool    
def scrap_url(url : str) -> str:
    """
Scrape a webpage and extract its main textual content.

Use this tool after obtaining a URL from a search result when more detailed
information is needed. The tool removes HTML tags, navigation menus,
advertisements, and other irrelevant elements to provide clean text for
research, summarization, and fact extraction.

Returns:
- Cleaned webpage content as plain text
"""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:1500]
    except Exception as e:
        return f"could not scrap URL: {str(e)}"
