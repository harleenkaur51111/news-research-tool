import os
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
newsapi_key = os.getenv("NEWSAPI_KEY")

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3,
    groq_api_key=groq_api_key
)

template = """
You are an AI assistant helping an equity research analyst. Given
the following query and the provided news article summaries, provide
an overall summary.

Query: {query}
Summaries: {summaries}
"""
prompt = PromptTemplate(template=template, input_variables=["query", "summaries"])

def get_news_articles(query):
    """Fetch articles from newsapi.org"""
    url = "https://newsapi.org/v2/everything"
    params = {
        "apiKey": newsapi_key,
        "q": query,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 10
    }
    response = requests.get(url, params=params)

    print("STATUS CODE:", response.status_code)
    print("RESPONSE TEXT (first 500 chars):", response.text[:500])

    if response.status_code != 200:
        return []

    try:
        data = response.json()
    except ValueError:
        return []

    return data.get("articles", [])

def summarize_articles(articles):
    """Combine article descriptions/content into one text block"""
    texts = []
    for article in articles:
        text = article.get("description") or article.get("title", "")
        if text:
            texts.append(text)
    return " ".join(texts)[:6000]

def get_summary(query):
    if not newsapi_key:
        return "Error: NEWSAPI_KEY not found. Check your .env file."
    articles = get_news_articles(query)
    if not articles:
        return "No articles found for this query (see terminal for debug info)."
    combined_text = summarize_articles(articles)
    chain = prompt | llm
    response = chain.invoke({"query": query, "summaries": combined_text})
    return response.content