from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_core.tools import tool


# ---------- Web Search ----------
search = DuckDuckGoSearchRun()

@tool
def search_tool(query: str) -> str:
    """Search the web for reliable information."""
    return search.run(query)


# ---------- Wikipedia ----------
wiki_api = WikipediaAPIWrapper(
    top_k_results=3,
    doc_content_chars_max=4000
)

wiki_tool = WikipediaQueryRun(api_wrapper=wiki_api)


# ---------- Save ----------
@tool
def save_tool(content: str) -> str:
    """Save research content to a file."""
    with open("research_output.txt", "w", encoding="utf-8") as f:
        f.write(content)
    return "Saved to research_output.txt"
