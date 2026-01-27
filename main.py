import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from schemas import ResearchResponse
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4,
)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional research assistant.

RULES:
- Use Wikipedia content when available
- Do NOT mix previous queries
- Produce VALID JSON ONLY
- Summary MUST be at least 500 words
- No markdown, no headings inside summary

{format_instructions}
""",
        ),
        (
            "human",
            """
Topic: {query}

Wikipedia content:
{wiki_context}

Web search content:
{search_context}
""",
        ),
    ]
).partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm


if __name__ == "__main__":
    query = input("What can I help you research? ").strip()

    wiki_context = wiki_tool.run(query)
    search_context = search_tool.run(query)

    raw_response = chain.invoke(
        {
            "query": query,
            "wiki_context": wiki_context,
            "search_context": search_context,
        }
    )

    print("\n===== RAW MODEL OUTPUT =====\n")
    print(raw_response.content)

    try:
        parsed = parser.parse(raw_response.content)

        print("\n===== STRUCTURED OUTPUT =====\n")
        print(json.dumps(parsed.model_dump(), indent=4))

        if "save" in query.lower():
            save_tool.invoke(json.dumps(parsed.model_dump(), indent=4))

    except Exception as e:
        print("\n Parsing failed")
        print(e)
